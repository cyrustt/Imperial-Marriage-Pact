import pandas as pd
import numpy as np
from math import sqrt
import random

numberOfPeople = 543

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

    def distance_to(self, other):
        bias = 1
        if self.preferred_gender != 'any' and self.preferred_gender != other.gender:
            bias *= 10
        if self.preferred_race != 'any' and set(self.preferred_race).isdisjoint(other.race):
            bias *= 10
        if abs(self.age - other.age) > self.preferred_age:
            bias *= 10
        return np.linalg.norm(self.answers - other.answers) * bias


def load_data(file_path: str):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.replace('\n', '', regex=True)
    
    indices = list(range(0, numberOfPeople))
    persons = {}
    
    print(df.columns)
    
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


def precompute_preferences(persons):
    preferences = [[] for _ in range(len(persons))]
    for person in persons.values():
        compatible = [(other.id, person.distance_to(other)) for other in persons.values() if other.id != person.id]
        preferences[person.id] = [id for id, _ in sorted(compatible, key=lambda x: x[1])]
    return preferences


def stable_matchings(preferences):
    marriages = [None] * numberOfPeople
    choice = 0
    while choice < numberOfPeople - 1:
        for person_id in range(numberOfPeople):
            if marriages[person_id] is None:
                target = preferences[person_id][choice]
                if marriages[target] is None:
                    marriages[person_id] = target
                else:
                    if preferences[target].index(person_id) < preferences[target].index(marriages.index(target)):
                        marriages[person_id] = target
                        marriages[marriages.index(target)] = None
        choice += 1
    return marriages


def find_compatibilities(participants, match_results):
    final_pairings = {}
    ignored_people = []
    
    def compatibility_score(proposer, receiver):
        distance = receiver.distance_to(proposer)
        max_distance = sqrt(len(receiver.answers) * (7 - 1) ** 2) * 5
        return max(0, 100 * (1 - distance / max_distance))
    
    for person in range(len(match_results)):
        if match_results[person] is None:
            ignored_people.append(participants[person])
        else:
            proposer = participants[person]
            receiver = participants[match_results[person]]
            final_pairings[proposer] = (receiver, compatibility_score(proposer, receiver))
    
    return final_pairings, ignored_people


def save_results_to_excel(compatibilities, ignored, output_file="best_match_results.xlsx"):
    matched_data = []
    seen_pairs = set()
    
    for proposer, (receiver, score) in compatibilities.items():
        pair = tuple(sorted([proposer.id, receiver.id]))
        if pair not in seen_pairs:
            seen_pairs.add(pair)
            matched_data.append([
                proposer.first_name, proposer.last_name, proposer.email, proposer.social,
                receiver.first_name, receiver.last_name, receiver.email, receiver.social,
                f"{score:.2f}%"
            ])
    
    unmatched_data = [[person.first_name, person.last_name, person.email, person.social] for person in ignored]
    
    matched_df = pd.DataFrame(matched_data, columns=[
        "Proposer First Name", "Proposer Last Name", "Proposer Email", "Proposer Social Media",
        "Receiver First Name", "Receiver Last Name", "Receiver Email", "Receiver Social Media",
        "Compatibility Score"
    ])
    
    unmatched_df = pd.DataFrame(unmatched_data, columns=["First Name", "Last Name", "Email", "Social Media"])
    
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        matched_df.to_excel(writer, sheet_name="Matched Pairs", index=False)
        unmatched_df.to_excel(writer, sheet_name="Unmatched", index=False)
    
    print(f"Best results saved to {output_file}")


if __name__ == "__main__":
    file_path = "Imperial Marriage Pact(1-545).xlsx"
    best_result = None
    best_compatibility_count = 0
    
    for _ in range(20):
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
