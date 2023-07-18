from collections import UserDict
from datetime import datetime, date
import re


class WrongPhone(Exception):
    pass


class WrongDate(Exception):
    pass


class Field:
    def __init__(self, value, required=False):
        self._value = value
        self.required = required
        if required and not value:
            raise ValueError("Required field is not provided.")

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self._value == other.value
        return False

    def __hash__(self):
        return hash(self._value)
    
    
class Name(Field):
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        self._value = val
        

class Phone(Field):

    @staticmethod
    def is_valid_phone(phone):
        match = re.search(r"^\+?[1-9][\d]{11}$", phone)
        return bool(match)

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        if self.is_valid_phone(val):
            self._value = val
        else:
            raise WrongPhone("You tried to enter an invalid phone number. " 
                             "Please check the value and try again")


class Birthday(Field):

    @staticmethod
    def is_valid_date(date):
        try:
            datetime.strptime(str(date), "%d.%m.%Y")
            return True
        except ValueError:
            return False

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        if self.is_valid_date(val):
            self._value = val
        else:
            raise WrongDate("Invalid date. Please enter birthday in format 'DD.MM.YYYY'.")


class Record:
    def __init__(self, name, phones=None, birthday=None):
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def __str__(self):
        phones = ", ".join([str(phone) for phone in self.phones])
        birthday = f"Birthday: {self.birthday}" if self.birthday.value else ""
        return f"{self.name.value}: {phones}. {birthday}"

    def __repr__(self):
        return str(self)

    def add_phone(self, phone: Phone):
        self.phones.append(phone)
        self.phones = list(set(self.phones))
        return f"Phone number {phone} for user {self.name.value} added successfully."

    def change_phone(self, old_number: Phone, new_number: Phone):
        if old_number not in self.phones:
            return f"Number {old_number} not found."
        else:
            phone_number_index = self.phones.index(old_number)
            self.phones[phone_number_index] = new_number
            return f"The phone number {old_number} for the user {self.name} "\
                f"has been changed to {new_number}"

    def delete_phone(self, phone):
        try:
            self.phones.remove(phone)
            return f"Phone number {phone} for user {self.name} deleted successfully."
        except ValueError:
            return f"Phone number {phone} for user {self.name} not found"

    def days_to_birthday(self):
        try:
            birthday = datetime.strptime(str(self.birthday), "%d.%m.%Y").date()
        except ValueError:
            return f"No birthday for user {self.name.value}"
        
        today = date.today()
        birthday = birthday.replace(year=today.year)
        if birthday < today:
            birthday = birthday.replace(year=today.year+1)
        result = (birthday - today).days
        birthday_str = birthday.strftime("%d %B")
        return f"The birthday of user {self.name} will be in {result} days, {birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self[record.name.value] = record

    def delete_record(self, name: Name):
        del self[name.value]

    def change_record(self, name, new_record):
        self[new_record.name.value] = new_record

    def __iter__(self):
        self.current_page = 1
        self.page_size = 10
        self.start_index = (self.current_page - 1) * self.page_size
        self.end_index = self.start_index + self.page_size
        return self
    
    def __next__(self):
        if self.start_index >= len(self.data):
            raise StopIteration
        
        page_records = list(self.data.values())[self.start_index:self.end_index]
        self.start_index = self.end_index
        self.end_index = self.start_index + self.page_size
        self.current_page += 1

        return page_records
    