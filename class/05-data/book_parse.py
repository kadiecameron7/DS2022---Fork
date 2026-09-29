import json

with open("data/book.json", "r") as f:
    data = json.load(f)

print(data["title"])
print(data["author"])
for genre in data["genres"]:
    print(genre)
