import csv
import re

import classes


def open_file(filename) -> classes.AddressBook:
    """Take as input filename. Return AddressBook"""
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

    return data


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
