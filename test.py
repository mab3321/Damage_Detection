import json

json_str = str({"name": "John", "is_active": false, "age": 30})

# Convert JSON string to dictionary
data = json.loads(json_str)

print(data)
