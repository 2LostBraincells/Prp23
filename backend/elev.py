from person import Person

class Elev(Person):
    """
    A class representing a student
    """
    slots = [
        '__grade', # Grade is used instead of class as class is a reserved keyword
        '__program',
        '__courses'
    ]


    def __init__(self, förnamn, efternamn, klass, program):
        """ 
        Initializes the student with the given first name, last name, class and program
        """

        super().__init__(förnamn, efternamn)
        self.__grade = klass
        self.__program = program
        self.__courses = set()

    
    @staticmethod
    def from_person(person: Person, klass: str, program: str):
        """
        Creates a student from a person object
        """

        student = Elev(person.first_name, person.last_name, klass, program)
        if hasattr(person, "_Person__pin"):
            student.set_pin(person.pin)
        if hasattr(person, "_Person__email"):
            student.set_email(person.email)
        if hasattr(person, "_Person__phone"):
            student.set_phone(person.phone_number)
        if hasattr(person, "_Person__address"):
            student.set_mailing_address(person.address, person.zip_code, person.city)
        return 

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


    def __str__(self):
        ret_str = super().__str__()
        if hasattr(self, "_Elev__class"):
            ret_str += f"Klass: {self.group}\n"
        if hasattr(self, "_Elev__program"):
            ret_str += f"Program: {self.program}\n"
        if hasattr(self, "_Elev__courses"):
            if self.__courses:
                ret_str += f"Kurser: {', '.join(self.courses)}\n"
            else:
                ret_str += "Kurser: Inga kurser\n"

        return ret_str


    @property
    def group(self):
        """
        Returns the group (the class) of the student
        """

        if not hasattr(self, "_Elev__class"):
            raise AttributeError("Class not set")

        return self.__grade


    @property
    def program(self):
        """
        Returns the promgam of the student
        """

        if not hasattr(self, "_Elev__program"):
            raise AttributeError("Program not set")

        return self.__program


    def change_class(self, klass):
        self.__grade = klass


    def change_program(self, program):
        self.__program = program


    def add_course(self, course):
        self.__courses.add(course)


    def remove_course(self, course):
        if course in self.__courses:
            self.__courses.remove(course)


    @property
    def courses(self):
        if not hasattr(self, "_Elev__courses"):
            raise AttributeError("No courses set")

        # Return a copy of the courses as to not allow direct modification
        return self.__courses.copy()
