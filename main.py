from collections import UserDict
from datetime import datetime, date
import pickle


# Base class representing a field with a value
class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __str__(self):
        return str(self.value)


# Subclass of Field representing a Name field
class Name(Field):
    def __init__(self, name):
        super().__init__(name)


# Subclass of Field representing a Phone field
class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone):
        if not (len(phone) == 10 and phone.isdigit()):
            raise ValueError("Phone number must be 10 digits and consist of digits only")
        self.__value = phone


# Subclass of Field representing a Birthday field
class Birthday(Field):
    def __init__(self, birthday):
        super().__init__(birthday)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, birthday):
        try:
            datetime.strptime(birthday, '%Y-%m-%d')
            self.__value = birthday
        except ValueError:
            raise ValueError("Invalid birthday format. Please use 'YYYY-MM-DD' format.")


# Class representing a record with a name and a list of phones
class Record:
    def __init__(self, name, phones=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        if phones:
            for phone in phones:
                self.add_phone(phone)
        self.birthday = None
        if birthday:
            self.birthday = Birthday(birthday)

    # Method to count days until the birthday
    def days_to_birthday(self):
        if self.birthday is None:
            return None
        today = date.today()
        birthday_date = date(*map(int, self.birthday.value.split("-")))
        next_birthday = birthday_date.replace(year=today.year)
        if today > next_birthday:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    # Method to add a phone to the record
    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

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

    # Method to find a phone number in the record
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        if self.birthday is not None:
            birthday_str = self.birthday.value
            days_until_birthday = self.days_to_birthday()
            return (f"Contact name: {self.name.value}, Phones: {phones_str}, Birthday: {birthday_str}, "
                    f"Days until birthday: {days_until_birthday} days")
        else:
            return f"Contact name: {self.name.value}, phones: {phones_str}, No birthday specified"


# Class representing an address book using a UserDict
class AddressBook(UserDict):

    # Method to add a record to the address book
    def add_record(self, record):
        self.data[record.name.value] = record

    # Method to find a record by parts name or phone in the address book
    def find(self, query):
        matching_contacts = []
        for note in self.values():
            if query.lower() in note.name.value.lower():
                matching_contacts.append(note)
            for phone in note.phones:
                if query.lower() in phone.value:
                    matching_contacts.append(note)
        return matching_contacts

    # Method to delete a record by name from the address book
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    # A method that returns a generator for records, which, in one iteration, returns representations for N records.
    def iterator(self, batch_size=2):
        record_keys = list(self.data)
        current_batch = 0
        while current_batch < len(record_keys):
            yield [self.data[record_keys[i]]
                   for i in range(current_batch, min(current_batch + batch_size, len(record_keys)))]
            current_batch += batch_size


class AddressBookFileManager:
    def __init__(self, filename):
        self.filename = filename

    def save(self, address_book):
        with open(self.filename, 'wb') as file:
            pickle.dump(address_book, file)

    def load(self):
        try:
            with open(self.filename, 'rb') as file:
                return pickle.load(file)
        except AttributeError:
            return None

    def __getstate__(self):
        attributes = self.__dict__.copy()
        return attributes

    def __setstate__(self, state):
        self.__dict__ = state


def main():
    filename = 'cont.txt'
    file_manager = AddressBookFileManager(filename)

    try:
        address_book = file_manager.load()
    except FileNotFoundError:
        address_book = AddressBook()
    while True:
        print("1. Додати контакт")
        print("2. Пошук контакту")
        print("3. Вийти")
        choice = input("Виберіть опцію: ")

        match choice:

            case "1":
                name = input("Введіть ім'я контакту: ")
                while True:
                    phone = input("Введіть номер телефону: ")
                    try:
                        Phone(phone)
                        break
                    except ValueError as e:
                        print(e)
                while True:
                    birthday = input("Введіть день народження (YYYY-MM-DD): ")
                    try:
                        Birthday(birthday)
                        break
                    except ValueError as e:
                        print(e)
                new_record = Record(name, [phone], birthday)
                address_book.add_record(new_record)
                file_manager.save(address_book)
                print("Контакт додано!")

            case "2":
                query = input("Введіть ім'я або номер телефону для пошуку: ")
                matching_contacts = address_book.find(query)
                if matching_contacts:
                    print(f"За Вашим запитом '{query}' знайдено такі контакти:")
                    for contact in matching_contacts:
                        print(contact)
                else:
                    print("Контакт не знайдено")

            case "3":
                break

if __name__ == "__main__":
    main()
