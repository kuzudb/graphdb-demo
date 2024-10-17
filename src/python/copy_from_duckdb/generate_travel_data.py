"""
Generate travel data for the persons and cities in `person.csv`
A person can only have travelled to cities in the file `person.csv`
"""

import csv
import random

# Fix random seed
random.seed(32457)

# Read data from person.csv
people = []
with open("travel/person.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        people.append((row[0], row[2]))  # Store name and city

# Generate travel data
travels = []
for _ in range(20):
    person = random.choice(people)
    destination = random.choice(people)[1]  # Choose a random city

    # Ensure person doesn't travel to their own city
    while destination == person[1]:
        destination = random.choice(people)[1]

    travels.append([person[0], destination])

# Write data to travel.csv
with open("travel/travel.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "travels_to"])
    writer.writerows(travels)

print("travel.csv has been generated successfully.")
