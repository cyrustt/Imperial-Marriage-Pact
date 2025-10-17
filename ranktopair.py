import math


class Person:
    def __init__(self, name, email, gender, race, age, genderPref, racePref, agePref, rank, partner):
        self.name = name
        self.email = email
        self.gender = gender
        self.race = race
        self.age = age
        self.genderPref = genderPref
        self.racePref = racePref
        self.agePref = agePref
        self.rank = rank
        self.partner = partner
        self.IndexOfPartner = None
        
    def AskOut(self, otherPerson):
        if otherPerson.partner == None or (otherPerson in self.rank and otherPerson.rank.index(self) < otherPerson.IndexOfPartner):
            self.partner = otherPerson
            self.IndexOfPartner = self.rank.index(otherPerson)
            otherPerson.partner = self
            otherPerson.IndexOfPartner = otherPerson.rank.index(self)
            return True
        else:
            return False
        

A = Person('A', None, None)
B = Person('B', None, None)
C = Person('C', None, None)

listOfMen = [A, B, C]

X = Person('X', (C, B, A), None)
Y = Person('Y', (A, B, C), None)
Z = Person('Z', (C, A, B), None)

A.rank = (Y, Z, X)
B.rank = (X, Y, Z)
C.rank = (Z, X, Y)

listOfWomen = [X, Y, Z]

Updated = True
counter = 0

while Updated:
    Updated = False
    for person in listOfMen:
        if person.partner == None and person.AskOut(person.rank[counter]):
            Updated = True
    
    counter += 1
        
        
for person in listOfMen:
    print(f"{person.name} paired with {person.partner.name} with compatability {(6- person.IndexOfPartner - person.partner.IndexOfPartner)/6*100}%")
            