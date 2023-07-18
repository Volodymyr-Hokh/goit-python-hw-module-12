import csv
import re

import classes


def open_file_and_check_name(name: str) -> tuple:
    """Take as input username. Return tuple with 
        AddressBook in which key is the name and value is the phone numbers 
        and bool value True if name already exist in dataframe, False otherwise."""
    try:
        with open("data.csv", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = classes.AddressBook()
            for row in reader:
                username = classes.Name(row["Name"])
                phones_str = re.sub(r"\[|\]|\ ", "",
                                    row["Phone numbers"]).split(",")
                phones = [classes.Phone(phone) for phone in phones_str]
                birthday = classes.Birthday(row["Birthday"])

                record = classes.Record(username, phones, birthday)
                data[record.name.value] = record

    except FileNotFoundError:
        data = classes.AddressBook()

    name_exists = bool(data.get(name))

    return (data, name_exists)


def write_to_csv(ab: classes.AddressBook, file_path: str):
    fieldnames = ["Name", "Phone numbers", "Birthday"]

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for record in ab.data.values():
            writer.writerow(
                {"Name": record.name,
                 "Phone numbers": record.phones,
                 "Birthday": record.birthday})
