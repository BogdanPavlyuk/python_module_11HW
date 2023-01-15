from collections import UserDict
from datetime import datetime, date


class Field:
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return self.value


class Name(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value.startswith('+380') and len(value) == 13:
            self.__value = value
        else:
            raise ValueError(
                print("Enter the phone number in the format: +380333333333"))


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value
      
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value:
            try:
                datetime.strptime(value, '%d.%m.%Y')
            except:
                raise ValueError('Enter the date of birth in the format dd.mm.yyyy')
        self.__value = value

class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone:
            self.phones.append(phone)
            
    def __str__(self) -> str:
        return f'User {self.name} - Phones: {", ".join([phone.value for phone in self.phones])}' \
               f' - Birthday: {self.birthday} '        

    def add_phone(self, phone: Phone):
        if isinstance(phone, Phone):
            self.phones.append(phone)
            return f"{phone.value} add success to contact {self.name.value}"
        return f"Sorry, phone must be a Phone instance"

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        self.phones[self.phones.index(old_phone)] = new_phone

    def days_to_birthday(self):
        if self.birthday:
            now_day = date.today()
            b_day = datetime.strptime(str(self.birthday), '%d.%m.%Y')
            birthday_day = date(year=now_day.year, month=b_day.month, day=b_day.day)
            if birthday_day < now_day:
                birthday_day = date(year=now_day.year + 1, month=b_day.month, day=b_day.day)
            return (birthday_day - now_day).days
        else:
            return 'Unknown birthday'


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, num: int = 2):
        page = 1
        counter = 0
        result = '\n'
        for i in self.data:
            result += f'{self.data[i]}\n'
            counter += 1
            if counter >= num:
                yield result
                result = ' ' * 40 + 'page ' + str(page) + '\n'
                counter = 0
                page += 1
        yield result


if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('+380982729332')
    birthday = Birthday('22.06.1987')
    rec = Record(name, phone, birthday)
    ab = AddressBook()
    ab.add_record(rec)

    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '+380982729332'

    print('All Ok)')
