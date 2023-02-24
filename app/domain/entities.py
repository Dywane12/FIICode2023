import itertools


class Patient:
    __auto_iterative_id = itertools.count()

    def __init__(self, first_name, last_name, phone_number, email, address, serie_buletin, cnp,
                 birth_date, marital_status, gender, medical_record_id, id=None):
        if id is None:
            self.__id = next(self.__auto_iterative_id)
        else:
            self.__id = id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__phone_number = phone_number
        self.__email = email
        self.__address = address
        self.__serie_buletin = serie_buletin
        self.__cnp = cnp
        self.__birth_date = birth_date
        self.__marital_status = marital_status
        self.__gender = gender
        self.__medical_record_id = medical_record_id

    @property
    def id(self):
        return self.__id

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def phone_number(self):
        return self.__phone_number

    @property
    def email(self):
        return self.__email

    @property
    def address(self):
        return self.__address

    @property
    def serie_buletin(self):
        return self.__serie_buletin

    @property
    def cnp(self):
        return self.__cnp

    @property
    def birth_date(self):
        return self.__birth_date

    @property
    def marital_status(self):
        return self.__marital_status

    @property
    def gender(self):
        return self.__gender

    @property
    def medical_record_id(self):
        return self.__medical_record_id

    @first_name.setter
    def first_name(self, value):
        self.__first_name = value

    @last_name.setter
    def last_name(self, value):
        self.__last_name = value

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = value

    @email.setter
    def email(self, value):
        self.__email = value

    @address.setter
    def address(self, value):
        self.__address = value

    @serie_buletin.setter
    def serie_buletin(self, value):
        self.__serie_buletin = value

    @cnp.setter
    def cnp(self, value):
        self.__cnp = value

    @birth_date.setter
    def birth_date(self, value):
        self.__birth_date = value

    @marital_status.setter
    def marital_status(self, value):
        self.__marital_status = value

    @gender.setter
    def gender(self, value):
        self.__gender = value

    @marital_status.setter
    def marital_status(self, value):
        self.__marital_status = value

    @gender.setter
    def gender(self, value):
        self.__gender = value

    @medical_record_id.setter
    def medical_record_id(self, value):
        self.__medical_record_id = value


class Doctor:
    __auto_iterative_id = itertools.count()

    def __init__(self, first_name, last_name, phone_number, email, address, birth_date, gender, consultation_schedule_office, consultation_schedule_away, assistants_schedule, id=None):
        if id is None:
            self.__id = next(self.__auto_iterative_id)
        else:
            self.__id = id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__phone_number = phone_number
        self.__email = email
        self.__address = address
        self.__birth_date = birth_date
        self.__gender = gender
        self.__consultation_schedule_office = consultation_schedule_office
        self.__consultation_schedule_away = consultation_schedule_away
        self.__assistants_schedule = assistants_schedule

    @property
    def id(self):
        return self.__id

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def phone_number(self):
        return self.__phone_number

    @property
    def email(self):
        return self.__email

    @property
    def address(self):
        return self.__address

    @property
    def birth_date(self):
        return self.__birth_date

    @property
    def gender(self):
        return self.__gender

    @property
    def consultation_schedule_office(self):
        return self.__consultation_schedule_office

    @property
    def consultation_schedule_away(self):
        return self.__consultation_schedule_away

    @property
    def assistants_schedule(self):
        return self.__assistants_schedule

    @first_name.setter
    def first_name(self, value):
        self.__first_name = value

    @last_name.setter
    def last_name(self, value):
        self.__last_name = value

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = value

    @email.setter
    def email(self, value):
        self.__email = value

    @address.setter
    def address(self, value):
        self.__address = value

    @birth_date.setter
    def birth_date(self, value):
        self.__birth_date = value

    @gender.setter
    def gender(self, value):
        self.__gender = value

    @consultation_schedule_office.setter
    def consultation_schedule_office(self, value):
        self.__consultation_schedule_office = value

    @consultation_schedule_away.setter
    def consultation_schedule_away(self, value):
        self.__consultation_schedule_away = value

    @assistants_schedule.setter
    def assistants_schedule(self, value):
        self.__assistants_schedule = value


class Consultation:
    __auto_iterative_id = itertools.count()

    def __init__(self, patient_id, doctor_id, time, id=None):
        if id is None:
            self.__id = next(self.__auto_iterative_id)
        else:
            self.__id = id
        self.__patient_id = patient_id
        self.__doctor_id = doctor_id
        self.__time = time

    @property
    def id(self):
        return self.__id

    @property
    def patient_id(self):
        return self.__patient_id

    @property
    def doctor_id(self):
        return self.__doctor_id

    @property
    def time(self):
        return self.__time

    @patient_id.setter
    def patient_id(self, value):
        self.__patient_id = value

    @doctor_id.setter
    def doctor_id(self, value):
        self.__doctor_id = value

    @time.setter
    def time(self, value):
        self.__time = value
