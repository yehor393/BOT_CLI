from abc import ABC, abstractmethod
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
            pickle.dump(address_book, file)  # Save the address book to a binary file.

    def load(self):
        try:
            with open(self.filename, 'rb') as file:
                return pickle.load(file)  # Load the address book from a binary file.
        except AttributeError:
            return None


class UserInterface(ABC):
    @abstractmethod
    def display_contacts(self, contacts):
        pass

    @abstractmethod
    def display_commands(self):
        pass

    @abstractmethod
    def get_user_input(self, prompt):
        pass


class ConsoleUserInterface(UserInterface):
    def display_contacts(self, contacts):
        print("Contacts:")
        for contact in contacts:
            print(contact)

    def display_commands(self):
        print("Available commands:")
        print("1. Add a contact")
        print("2. Search for a contact")
        print("3. Show all contacts")
        print("4. Exit")

    def get_user_input(self, prompt):
        return input(prompt)


# Define a main function for the program.
def main(user_interface):
    filename = 'contact.txt'
    file_manager = AddressBookFileManager(filename)

    try:
        address_book = file_manager.load()  # Attempt to load the address book from the file.
    except FileNotFoundError:
        address_book = AddressBook()  # Create a new address book if the file doesn't exist.

    while True:
        user_interface.display_commands()
        choice = user_interface.get_user_input("Choose an option: ")

        if choice == "1":
            name = input("Enter the contact's name: ")
            while True:
                phone = input("Enter the phone number: ")
                try:
                    Phone(phone)  # Validate the phone number.
                    break
                except ValueError as e:
                    print(e)
            while True:
                birthday = input("Enter the date of birth (YYYY-MM-DD): ")
                try:
                    Birthday(birthday)  # Validate the date of birth.
                    break
                except ValueError as e:
                    print(e)
            new_record = Record(name, [phone], birthday)
            address_book.add_record(new_record)
            file_manager.save(address_book)  # Save the updated address book.
            print("Contact added!")

        elif choice == "2":
            query = input("Enter a name or phone number to search for: ")
            matching_contacts = address_book.find(query)
            if matching_contacts:
                print(f"Contacts found for your query '{query}':")
                for contact in matching_contacts:
                    print(contact)
            else:
                print("Contact not found")

        elif choice == "3":
            user_interface.display_contacts(address_book.values())

        elif choice == "4":
            break

        else:
            print("Invalid choice. Please choose a valid option.")


# Run the main function if this script is executed.
if __name__ == "__main__":
    console_ui = ConsoleUserInterface()
    main(console_ui)
