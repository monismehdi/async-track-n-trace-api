import json

shipments_db = {}
# print(f"Initial Shipments DB: {shipments_db}")

# print("Loading shipments from shipments.json...")
with open("shipments.json", "r") as f:
    data = json.load(f)

for value in data:
    shipments_db[value["id"]] = value

#print(f"Loaded {len(shipments_db)} shipments.")
# print(f"Shipments DB: {shipments_db}")

def save_shipments():
    with open("shipments.json", "w") as json_file:
        json.dump(
            list(shipments_db.values()),
            json_file,
            indent=4)