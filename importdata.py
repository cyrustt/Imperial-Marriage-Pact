import csv
from ranktopair import Person

def create_sets:

    with open('marriagepacttest.csv', 'r', encoding="utf-8-sig") as csvfile:
        
        PeopleList = []
        
        reader = csv.reader(csvfile)
        
        firstline = next(reader)
        
        for line in reader:
            PeopleList.append(Person())