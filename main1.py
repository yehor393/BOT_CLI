from collections import UserDict


# Base class representing a field with a value
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Subclass of Field representing a Name field
class Name(Field):
    def __init__(self, name):
        super().__init__(name)


# Function to check if a phone number is valid (10 digits)
def is_valid_phone(phone):
    return len(phone) == 10 and phone.isdigit()


# Subclass of Field representing a Phone field
class Phone(Field):
    def __init__(self, phone):
        if not is_valid_phone(phone):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(phone)


# Class representing a record with a name and a list of phones
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    # Method to add a phone to the record
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # Method to remove a phone from the record
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break
        else:
            raise ValueError("Phone number not found")

    # Method to edit an existing phone number in the record
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if old_phone == p.value:
                p.value = new_phone
                break
        else:
            raise ValueError("Phone number not found")

        if not is_valid_phone(new_phone):
            raise ValueError("New phone number must be 10 digits")

    # Method to find a phone number in the record
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


# Class representing an address book using a UserDict
class AddressBook(UserDict):
    # Method to add a record to the address book
    def add_record(self, record):
        self.data[record.name.value] = record

    # Method to find a record by name in the address book
    def find(self, name):
        if name in self.data:
            return self.data[name]
        return None

    # Method to delete a record by name from the address book
    def delete(self, name):
        if name in self.data:
            del self.data[name]
