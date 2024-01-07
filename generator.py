import faker
import json
import random

fake = faker.Faker()

def numbers():
    return [str(fake.random_number(digits=10)) for i in range(random.choice([1, 1, 2]))]
def generate_data(num_entries):
    data = {"admin": {"theme": "6", "language": "english"}, "Aa Disclaimer": [["NA"], "This data was randomly generated"]}
    for _ in range(num_entries):
        name = fake.name()
        note = fake.sentence()
        data[name] = [numbers(), note]
    return data

generated_data = generate_data(100)
with open("phonebank.json", "w") as file:
    json.dump(generated_data, file)
