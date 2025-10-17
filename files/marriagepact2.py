import pandas as pd
import numpy as np
from math import sqrt
from typing import List, Dict, Tuple
import random

numberOfPeople = 532


class Person:
    def __init__(self, first_name, last_name, id, gender, race, age, preferred_gender, preferred_race, preferred_age, answers, email, social):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.gender = gender
        self.race = race
        self.age = age
        self.preferred_gender = preferred_gender
        self.preferred_race = preferred_race
        self.preferred_age = preferred_age
        self.answers = np.array(answers)
        self.email = email
        self.social = social

    def __str__(self):
        return f"{self.first_name} {self.last_name} with id = {self.id}"

    def is_compatible_with_gender(self, other):
        return (
            (self.preferred_gender == 'any' or self.preferred_gender == other.gender) 
        )
        
    def is_compatible_with_race(self, other):
        return (
            ('any' in self.preferred_race or not set(self.preferred_race).isdisjoint(other.race)) 
        )
        
    def is_compatible_with_age(self, other):
        return (
            (abs(self.age - other.age) <= self.preferred_age)
        )

    def distance_to(self, other):
        
        bias = 1
            
        if not (self.is_compatible_with_gender(other) and other.is_compatible_with_gender(self)):
            bias *= 10

        if not (self.is_compatible_with_race(other) and other.is_compatible_with_race(self)):
            bias *= 10

        if not (self.is_compatible_with_age(other) and other.is_compatible_with_age(self)):
            bias *= 10

            
        return np.linalg.norm(self.answers - other.answers)*bias


def load_data(file_path: str):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.replace('\n', '', regex=True)
    
    indices = list(range(0, numberOfPeople))
    persons = {}
    
    
    for _, row in df.iterrows():
        n = random.choice(indices)
        indices.remove(n)
        
        persons[n] = Person(
                first_name=row['FirstName'],
                last_name=row['LastName'],
                id=n,
                gender=row['Gender'].lower(),
                race=row['Race'].lower(),
                age=row['Age'],
                preferred_gender=row['Preferredgender'].lower(),
                preferred_race=row['Preferredrace'].lower(),
                preferred_age=row['Preferredage'],
                answers=[row[f'q{i}'] for i in range(1, 50)],
                email=row['email2'],
                social=row['SocialMedia']
            )  
    return persons


def precompute_preferences(persons: Dict):
    preferences = [0]*len(persons)
    for person in persons.values():
        compatible = []
        
        for other in persons.values():
            if other.id == person.id:
                continue
            
            compatible.append((other.id, person.distance_to(other)))
             
        preferences[person.id] = [id for id, _ in sorted(compatible, key=lambda x: x[1])]
    return preferences
 

def stable_matchings(preferences: List[List[int]]) -> List[int]:
    
    marriages = [None] * numberOfPeople
            
    choice = 0
    
    # loop to assign to first, second, third ... choice
    while choice<numberOfPeople-1:

        
        for person_id in range(numberOfPeople):
            # checks that the person were dealing with doesnt already have a partner
            target = preferences[person_id][choice]
            if marriages[person_id] == None and person_id not in marriages:
                if marriages[target] != None:
                    continue 
                
                # checks if the target has a partner, and match if not
                if target not in marriages :
                    marriages[person_id] = target

                # if someone else chose the target, we now see who the target prefers 
                else:
                    if preferences[target].index(person_id) < preferences[target].index(marriages.index(target)):
                        marriages[person_id] = target
                        marriages[marriages.index(target)] = None
 
                        
            #print(f"Person {person_id} proposing to {target}")
            #print(f"Marriages: {marriages}")
            #print(f"Updated: {Updated}, Choice Level: {choice}")
             
        choice += 1

    return marriages
        

def find_compatibilities(participants, match_results):
    # adding compatibility scores
    final_pairings = {}
    ignored_people = []
    length = len(match_results)
    
    def compatibility_score(proposer, receiver):
        distance = receiver.distance_to(proposer)
        max_distance = sqrt(len(receiver.answers) * (7 - 1) ** 2)*5 # Max possible distance
        return max(0, 100 * (1 - distance / max_distance))  # Convert to percentage
    
    for person in range(length):
        if match_results[person] == None and person not in match_results:
            ignored_people.append(participants[person])
        elif match_results[person] != None :
            proposer = participants[person]
            receiver = participants[match_results[person]]
            final_pairings[proposer] = (receiver, compatibility_score(proposer, receiver))
            
    return final_pairings, ignored_people
        

def save_results_to_excel(compatibilities, ignored, output_file="match_results.xlsx"):
    matched_data = []
    seen_pairs = set()
    
    for proposer, (receiver, score) in compatibilities.items():
        pair = tuple(sorted([proposer.id, receiver.id]))  # Ensure unique pairs
        
        if pair not in seen_pairs:
            seen_pairs.add(pair)
            matched_data.append([
                proposer.first_name, proposer.last_name, proposer.id, proposer.email, proposer.social,
                receiver.first_name, receiver.last_name, receiver.id, receiver.email, receiver.social,
                f"{score:.2f}%"
            ])
    
    unmatched_data = [[person.first_name, person.last_name, person.id, person.email, person.social] for person in ignored]
    
    # Creating DataFrames
    matched_df = pd.DataFrame(matched_data, columns=[
        "Proposer First Name", "Proposer Last Name", "Proposer ID", "Proposer Email", "Proposer Social",
        "Receiver First Name", "Receiver Last Name", "Receiver ID", "Receiver Email", "Receiver Social",
        "Compatibility Score"
    ])
    
    unmatched_df = pd.DataFrame(unmatched_data, columns=["First Name", "Last Name", "ID", "Email", "Social"])
    
    # Writing to Excel with multiple sheets
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        matched_df.to_excel(writer, sheet_name="Matched Pairs", index=False)
        unmatched_df.to_excel(writer, sheet_name="Unmatched", index=False)
    
    print(f"Results saved to {output_file}")

# Call the function after generating compatibilities



# Example usage
if __name__ == "__main__":
    file_path = "Imperial Marriage Pact(1-545).xlsx"
    best_result = None
    best_compatibility_count = 0
    
    for _ in range(20):
        print(f"running {_}...")
        participants = load_data(file_path)
        preferences = precompute_preferences(participants)
        match_results = stable_matchings(preferences)
        compatibilities, ignored = find_compatibilities(participants, match_results)
        
        high_compatibility_count = sum(1 for (_, score) in compatibilities.values() if score >= 80)
        
        if high_compatibility_count > best_compatibility_count:
            best_compatibility_count = high_compatibility_count
            best_result = (compatibilities, ignored)
    
    if best_result:
        save_results_to_excel(*best_result)


'''
def stable_matching(persons: List[Person], preferences: List[List[int]]) -> Dict[str, Tuple[str, float]]:
    # add shuffle here
    free_people = {person.id for person in persons}
    proposals = {person.id: [] for person in persons}
    matches = {}
    compatibility_scores = {}

    while free_people:
        person_id = free_people.pop()

        if preferences[person_id]:
            propose_to = preferences[person_id].pop(0)
            proposals[propose_to].append(person_id)

        for receiver_id, proposers in proposals.items():
            if not proposers:
                continue

            receiver = next(p for p in persons if p.id == receiver_id)

            def compatibility_score(proposer_name):
                proposer = next(p for p in persons if p.name == proposer_name)
                distance = receiver.distance_to(proposer)
                max_distance = sqrt(len(receiver.answers) * (7 - 1) ** 2)  # Max possible distance
                return 100 * (1 - distance / max_distance)  # Convert to percentage

            if receiver_id not in matches:
                # Receiver accepts the best proposal
                best_match = min(proposers, key=compatibility_score)
                matches[receiver_id] = best_match
                compatibility_scores[(receiver_id, best_match)] = compatibility_score(best_match)
            else:
                # Receiver chooses between the current match and new proposals
                current_match = matches[receiver_id]
                best_match = min(proposers + [current_match], key=compatibility_score)
                matches[receiver_id] = best_match
                compatibility_scores[(receiver_id, best_match)] = compatibility_score(best_match)

            # Update matches to avoid duplicates
            for proposer in proposers:
                if proposer != best_match:
                    free_people.add(proposer)
                else:
                    matches.pop(proposer, None)

        # Clear proposals for the next round
        proposals = {person.name: [] for person in persons}

    # Create a unidirectional matching dictionary with compatibility scores
    stable_matches = {
        proposer: (receiver, compatibility_scores[(receiver, proposer)])
        for receiver, proposer in matches.items()
    }
    return stable_matches
'''