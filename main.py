from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


def is_valid_phone(phone):
    return len(phone) == 10 and phone.isdigit()


class Phone(Field):
    def __init__(self, phone):
        if not is_valid_phone(phone):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(phone)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break
        else:
            raise ValueError("Phone number not found")

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if old_phone == p.value:
                p.value = new_phone
                break
        else:
            raise ValueError("Phone number not found")

        if not is_valid_phone(new_phone):
            raise ValueError("New phone number must be 10 digits")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]
