import datetime
import sqlite3
from typing import Union
import re

EVAL_VALUES = [0, 1, 2, 3, 4, 6, 7, 8, 9, 0]

# tagen från https://support.boldsign.com/kb/article/15962/how-to-create-regular-expressions-regex-for-email-address-validation
email_validator = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$')
# Tagen från någon random stackoverflow post
phone_validator = re.compile(r'^([+]46)\s*(7[0236])\s*(\d{4})\s*(\d{3})$')
# Tagen från chatgpt :^)
postcode_validator = re.compile(r'^(\d{3} ?\d{2}|SE-\d{3} ?\d{2})$')


"""
------------------
| Birthday class |
------------------
"""
class Birthday:
    """
    A class representing a birthday
    """
    slots = [
        '__datetime'
    ]

    def __init__(self, date: datetime.datetime):
        """
        Initializes the birthday with the given year, month and day
        """

        self.__datetime = date


    def __setattr__(self, name, value):
        """
        Prevents setting slots directly, making the class immutable to some extent
        """

        if hasattr(self, name):
            raise ValueError("Cannot set fields directly")

        self.__dict__[name] = value


    def __delattr__(self, name: str):
        """
        Prevents deleting slots directly
        """

        if hasattr(self, name):
            raise ValueError("Cannot delete fields")


    def __str__(self):
        """
        Returns the date as a string
        """

        return self.__datetime.strftime("%a %d %b %Y") + ", " + str(self.get_age()) + " years old"


    def _sql_format(self):
        """
        Returns the birthdate as a string in the format YYYY-MM-DD
        """

        return self.__datetime.strftime("%Y-%m-%d")



    def get_age(self):
        current_date = datetime.datetime.now()
        return current_date.year - self.__datetime.year - \
               ((current_date.month, current_date.day) < (self.__datetime.month, self.__datetime.day))



"""
-----------------
| Person class |
-----------------
"""
class Person:
    """
    A class representing a person
    """
    slots = [
        '__förnamn', 
        '__efternamn', 
        '__pin', 
        '__email', 
        '__phone', 
        '__address', 
        '__birthday'
    ]

    def __init__(self, förnamn, efternamn):
        """
        Initializes the person with the given first name and last name
        """

        self.__förnamn = förnamn
        self.__efternamn = efternamn



    def _build_Person_string(self):
        """
        Builds the string representation of the person
        """

        ret_str = f"Name: {self.full_name}\n"
        if hasattr(self, "_Person__pin"):
            ret_str += f"Pin: {self.pin}\n"
        if hasattr(self, "_Person__email"):
            ret_str += f"Email: {self.email}\n"
        if hasattr(self, "_Person__phone"):
            ret_str += f"Phone: {self.phone_number}\n"
        if hasattr(self, "_Person__address"):
            ret_str += f"Address: {self.address}\n"
        if hasattr(self, "_Person__birthday"):
            ret_str += f"Birthday: {self.birthday}\n"

        return ret_str


    def __str__(self):
        """
        Returns the string representation of the person
        """

        return self._build_Person_string()


    def __setattr__(self, name, value):
        """
        Prevents setting slots directly, making the class immutable to some extent
        """

        if hasattr(self, name):
            raise ValueError("Cannot set slots directly")

        self.__dict__[name] = value


    def __delattr__(self, name: str):
        """
        Prevents deleting slots directly
        """

        if hasattr(self, name):
            raise ValueError("Cannot delete slots")


    def set_pin(self, pin: str):
        """
        Sets the pin of the person if it is valid
        """

        if not self.__validate_pin(pin):
            raise ValueError("Invalid pin")

        birthday = self.__parse_birthday(pin)

        if not birthday:
            raise ValueError("Invalid birthday")

        self.__pin = pin
        self.__birthday = birthday

        return True



    def set_email(self, email: str):
        """
        Sets the email of the person if it is valid.

        Raises a ValueError if the email is invalid
        """

        if not email_validator.match(email):
            raise ValueError("Invalid email")

        self.__email = email


    def set_mailing_address(self, gatuadress: str, postnummer: Union[str, int], ort: str):
        """
        Sets the address of the person

        Raises a ValueError if the postnummer is invalid
        """

        self.__address = Postadress(gatuadress, postnummer, ort)


    def set_phone(self, phone: str):
        """
        Sets the phone number of the person if it is valid
        """
        
        if phone_validator.match(phone):
            raise ValueError("Invalid phone number")
        
        self.__phone = phone


    @property
    def full_name(self):
        """
        Returns the full name of the person

        Raises a ValueError if the name is not set
        """

        if not hasattr(self, "_Person__förnamn") or not hasattr(self, "_Person__efternamn"):
            raise ValueError("No name set")

        return f"{self.__förnamn} {self.__efternamn}"


    @property
    def first_name(self):
        """
        Returns the first name of the person

        Raises a ValueError if the name is not set
        """

        if not hasattr(self, "_Person__förnamn"):
            raise ValueError("No name set")

        return self.__förnamn


    @property
    def last_name(self):
        """
        Returns the first name of the person

        Raises a ValueError if the name is not set
        """

        if not hasattr(self, "_Person__förnamn"):
            raise ValueError("No name set")

        return self.__efternamn


    @property
    def email(self):
        """
        Returns the email of the person

        Raises a ValueError if the email is not set
        """
    
        if not hasattr(self, "_Person__email"):
            raise ValueError("No email set")

        return self.__email


    @property
    def phone_number(self):
        """
        Returns the phone number of the person

        raises a ValueError if the phone number is not set
        """
        
        if not hasattr(self, "_Person__phone"):
            raise ValueError("No phone number set")

        return self.__phone


    @property
    def mailing_address(self):
        """
        Returns the address of the person

        Raises a ValueError if the address is not set
        """

        if not hasattr(self, "_Person__address"):
            raise ValueError("No mailing address set")

        return self.__address


    @property
    def address(self):
        """
        Returns the gatuadress of the person

        Raises a ValueError if the address is not set
        """
        
        if not hasattr(self, "_Person__address"):
            raise ValueError("No address set")

        return self.__address.gatuadress


    @property
    def zip_code(self):
        """
        Returns the postnummer of the person

        Raises a ValueError if the address is not set
        """

        if not hasattr(self, "_Person__address"):
            raise ValueError("No address set")

        return self.__address.postnummer


    @property
    def city(self):
        """
        Returns the ort of the person

        Raises a ValueError if the address is not set
        """

        if not hasattr(self, "_Person__address"):
            raise ValueError("No address set")

        return self.__address.ort


    @property
    def birthday(self):
        """
        Returns the birthday of the person

        Raises a ValueError if the birthday is not set
        """
        if not hasattr(self, "_Person__birthday"):
            raise ValueError("No pin set")

        return self.__birthday


    @property
    def pin(self):
        """
        Returns the pin of the person

        Raises a ValueError if the pin is not set
        """
        if not hasattr(self, "_Person__pin"):
            raise ValueError("No pin set")

        return self.__pin


    @property
    def age(self):
        """
        Returns the age of the person

        Raises a ValueError if the birthday is not set
        """
        if not hasattr(self, "_Person__birthday"):
            raise ValueError("No birthday set")

        return self.__birthday.get_age()

    @staticmethod
    def __parse_birthday(pin: str) -> Birthday | None:
        """
        Parses the birthday from the pin

        returns a Birthday object if the pin is valid and birthday are valid, otherwise None
        """
        current_date = datetime.datetime.now()

        current_year = current_date.year
        current_century = current_year - current_year % 100

        year_size = 2 if len(pin) == 10 else 4

        pin_year = int(pin[0:year_size])
        pin_month = int(pin[year_size:year_size + 2])
        pin_day = int(pin[year_size + 2:year_size + 4])

        pin_date = datetime.datetime(pin_year if len(pin) == 12 else pin_year + current_century, 
                                     pin_month, pin_day)

        if pin_date > current_date:
            if len(pin) == 10:
                pin_date = datetime.datetime(pin_year + current_century - 100, pin_month, pin_day)
            else:
                return None

        return Birthday(pin_date)

    
    @staticmethod
    def __validate_pin(pin: str) -> bool:
        """
        Validates the pin and returns true if it is valid
        """
        valid_chars = pin.isdigit() and pin.isascii()
        valid_length = len(pin) in [10, 12]
        if not (valid_chars and valid_length):
            return False

        sum = 0
        for (i, n) in (enumerate(map(int, pin))):
            sum += (n + EVAL_VALUES[n]) if i % 2 == 0 else n

        if sum % 10 != 0:
            return False

        return True

    
    def _database_insert(self, cursor: sqlite3.Cursor):
        fields = []
        values = []

        fields.append("name")
        values.append(self.full_name)

        if hasattr(self, "_Person__pin"):
            fields.append("personal_id")
            values.append(self.pin)

        if hasattr(self, "_Person__email"):
            fields.append("email")
            values.append(self.email)

        if hasattr(self, "_Person__phone"):
            fields.append("phone_number")
            values.append(self.phone_number)

        if hasattr(self, "_Person__address"):
            fields.append("address")
            values.append(self.address)

            fields.append("zip_code")
            values.append(self.zip_code)

            fields.append("city")
            values.append(self.city)

        if hasattr(self, "_Person__birthday"):
            fields.append("birthday")
            values.append(self.birthday._sql_format())

        query = f"INSERT INTO person ({', '.join(fields)}) VALUES ({', '.join(['?' for _ in fields])})"

        cursor.execute(query, values)



    def _database_update(self, cursor: sqlite3.Cursor, **kwargs):
        pass


    def _database_delete(self, cursor: sqlite3.Cursor):
        pass


"""
---------------------
| Postadress class |
---------------------
"""
class Postadress:
    """
    A class holding all the information about a postadress
    """
    slots = [
        '__gatuadress',
        '__postnummer',
        '__ort'
    ]

    def __init__(self, gatuadress: str, postnummer: str | int, ort: str):
        """
        Initializes the postadress with the given gatuadress, postnummer and ort
        """

        postnummer = str(postnummer)

        if not postcode_validator.match(postnummer):
            raise ValueError("Invalid postnummer")

        postnummer = int(re.sub(r'\D', '', postnummer))

        self.gatuadress = gatuadress
        self.postnummer = postnummer
        self.ort = ort


    def __setattr__(self, name, value):
        """
        Prevents setting slots directly, making the class immutable to some extent
        """

        if hasattr(self, name):
            raise ValueError("Cannot set fields directly")

        self.__dict__[name] = value


    def __delattr__(self, name: str):
        """
        Prevents deleting slots directly
        """

        if hasattr(self, name):
            raise ValueError("Cannot delete fields")


    def __iter__(self):
        yield self.gatuadress
        yield self.postnummer
        yield self.ort


    def __str__(self):
        return f"{self.gatuadress}, {self.postnummer} {self.ort}"


