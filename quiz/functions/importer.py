import yaml

# Load the existing YAML data
with open("db.yaml", "r", encoding="utf8") as file:
    yaml_data = yaml.safe_load(file)

date = input("Date:")
while True:
    wde = input("Word DE:")
    wel = input("Word EL:")

    new_entry = {
        "date": date,
        "translations": {"de": wde, "el": wel},
    }

    yaml_data["words"].append(new_entry)

    with open("db.yaml", "w", encoding="utf8") as file:
        yaml.safe_dump(yaml_data, file, allow_unicode=True)

print("")
