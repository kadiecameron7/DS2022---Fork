import json

rows = [
    {"repo_name": "json-practice", "repo_url": "https://github.com/nmagee/json-practice/"},
    {"repo_name": "DS2022", "repo_url": "https://github.com/ksiller/DS2022"},
]
print(json.dumps(rows, indent=2))