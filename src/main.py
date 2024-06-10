from person import *
from elev import *
from sqlite import *

def main():
    print(Person.__doc__)

    db = Database("elever.db")

    person1 = Person("Elmer", "Brännström")
    person1.set_pin("0603179276")
    person1.set_email("elmer.brannstrom@gmail.com")
    person1.set_phone("0725438394")
    person1.set_mailing_address("Sandåsvägen 37", 90360, "Umeå")

    person2 = Person("Kalle", "Anka")
    person2.set_pin("0610092454")
    person2.set_email("email@email.com")

    print(person1)
    print(person2)

    db.insert(person1)
    db.insert(person2)

    person2.set_mailing_address("Slottet 37", 90360, "Umeå")

    elev1 = Elev("Elmer", "Brännström", "T22a", "Teknik")
    
    print("\n")
    print(elev1)

    elev1.set_pin("0603179276")
    elev1.set_email("elmer.brannstrom@gmail.com")
    elev1.set_phone("0725438394")
    elev1.set_mailing_address("Sandåsvägen 37", 90360, "Umeå")

    print("\n")
    print(elev1)

    elev1.add_course("Matematik")
    elev1.add_course("Fysik")
    elev1.add_course("Kemi")
    elev1.add_course("Engelska")

    print("\n")
    print(elev1)

    pass


if __name__ == "__main__":
    main()
