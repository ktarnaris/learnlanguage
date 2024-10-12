import os

# File to store translations
FILENAME = "db.yaml"


def load_translations():
    # If the file exists, load the current translations
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            return file.read()
    return ""


def save_translation(date, de, el):
    # Prepare the translation text format
    translation_entry = (
        f"- date: {date}\n  translations:\n    de: {de}\n    el: {el}\n\n"
    )

    # Append the new translation to the file
    with open(FILENAME, "a") as file:
        file.write(translation_entry)

    print(f"Translation added: Date: {date}, German: {de}, Greek: {el}")


def main():
    print("Welcome to the Translation App!")

    date = input("Enter the date (YYYY-MM-DD): ")
    while True:
        # Take user input for date, German (de) and Greek (el) translations
        de = input("Enter the German translation (de): ")
        el = input("Enter the Greek translation (el): ")

        # Add the new translation
        save_translation(date, de, el)

        # # Ask the user if they want to continue
        # cont = (
        #     input("Do you want to add another translation? (yes/no): ").strip().lower()
        # )
        # if econt not in ("yes", ""):
        #     break


if __name__ == "__main__":
    main()
