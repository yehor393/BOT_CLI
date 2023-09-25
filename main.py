from collections import UserDict
from datetime import datetime, date


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
        return self.__phone

    @value.setter
    def value(self, phone):
        if not (len(phone) == 10 and phone.isdigit()):
            raise ValueError("Phone number must be 10 digits and consist of digits only")
        self.__phone = phone


# Subclass of Field representing a Birthday field
class Birthday(Field):
    def __init__(self, birthday):
        self.__birthday = None
        super().__init__(birthday)

    @property
    def value(self):
        return self.__birthday

    @value.setter
    def value(self, birthday):
        try:
            datetime.strptime(birthday, '%Y-%m-%d')
            self.__birthday = birthday
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
        birthday_date = self.birthday.value
        birthday_date = date(*map(int, birthday_date.split("-")))
        next_birthday = birthday_date.replace(year=today.year)
        if today > next_birthday:
            next_birthday = next_birthday.replace(year=today.year + 1)
        days_until_birthday = (next_birthday - today).days
        return days_until_birthday

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
        phones_str = '; '.join(p.value for p in self.phones if p.value is not None)
        if self.birthday is not None:
            birthday_str = f'Birthday: {self.birthday.value}'
            days_until_birthday = self.days_to_birthday()
            return (f"Contact name: {self.name.value}, phones: {phones_str}, {birthday_str}, "
                    f"Days until birthday: {days_until_birthday} days")
        else:
            return f"Contact name: {self.name.value}, phones: {phones_str}, No birthday specified"


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

    # A method that returns a generator for records, which, in one iteration, returns representations for N records.
    def iterator(self, batch_size=2):
        record_keys = list(self.data)
        current_batch = 0
        while current_batch < len(record_keys):
            yield [self.data[record_keys[i]]
                   for i in range(current_batch, min(current_batch + batch_size, len(record_keys)))]
            current_batch += batch_size


# Створюємо об'єкт класу AddressBook
address_book = AddressBook()

# Створюємо об'єкти класу Record з іменем, номерами телефонів та днем народження
record1 = Record("John Doe", ["1234567890", "9876543210"], "2000-01-01")
record2 = Record("Jane Smith", ["1111111111", "2222222222"])
record3 = Record("Bob Johnson", ["3333333333"], "1995-05-05")

# Додаємо записи в адресну книгу
address_book.add_record(record1)
address_book.add_record(record2)
address_book.add_record(record3)

# Використовуємо пагінацію для виведення записів з адресної книги
iterator = address_book.iterator(batch_size=2)
while True:
    try:
        batch = next(iterator)
        for records in batch:
            print(records)
    except StopIteration:
        break
