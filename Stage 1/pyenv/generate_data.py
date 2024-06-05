from random import random, randint, choice
from random_address import real_random_address
import data_gen
import rand_data

generated_ids = set()
data_gen.weights()


class Person:
    count = 0

    def __init__(self) -> None:
        self.empId = self.count
        Person.count += 1
        self.first_name = choice(rand_data.first_names)
        self.last_name = choice(rand_data.last_names)
        self.birthdate = f'{randint(1950, 2003)}/{randint(1, 12)}/{randint(1, 28)}'
        self.empDate = f'{randint(1990, 2023)}/{randint(1, 12)}/{randint(1, 28)}'
        self.address = real_random_address()
        self.address = f"{self.address['address1']}, {self.address['city']}, {self.address['state']}, {self.address['postalCode']}"
        self.address = self.address.replace("'", "")

    @classmethod
    def get_wage(cls, lower, upper):
        return randint(lower, upper)


_luggageID = 1_000_000_000


def pilot_wage(flight_hours):
    base_salary = 5000 * 12
    if flight_hours <= 2000:
        wage = base_salary + flight_hours * 15
    elif flight_hours <= 5000:
        wage = (base_salary + flight_hours * 15) + ((flight_hours - 2000) * 2)
    else:
        wage = (base_salary + flight_hours * 15) + ((flight_hours - 5000) * 0.1)
    return wage


def random_luggage():
    global _luggageID
    # tag (id) unique integer
    tag = _luggageID
    _luggageID += randint(1, 10)

    # Random weight from 0-50 rounded to 2 decimal places
    weight = round(random() * 50.0, 2)

    # type cargo_type
    cargo_type = choice(rand_data.luggage_types)

    # between N-100AA and N-999ZZ
    aircraft_rn = data_gen.air_reg_code()

    return f'INSERT INTO luggage ("tag", "weight", "type", "aircraft_rn") VALUES ({tag}, {weight}, \'{cargo_type}\', \'{aircraft_rn}\');'


def random_carousel():
    carousel_number, iata, capacity, terminal = data_gen.carousel()

    return f'INSERT INTO carousel ("carousel_id", "capacity", "terminal", "iata") VALUES ({carousel_number}, {capacity}, {terminal}, \'{iata}\');'

def random_carousel_aircraft():
    # between N-100AA and N-999ZZ
    aircraft_rn = data_gen.air_reg_code()
    if aircraft_rn is not None:
        rand_data.FLEET.remove(aircraft_rn)

    cid, rid = data_gen.assign_aircraft(aircraft_rn)

    return f'INSERT INTO carousel_aircraft ("carousel_id", "aircraft_rn") VALUES ({cid}, \'{rid}\');'


FLIGHT_HOURS_YEARLY_AVERAGE = 840  # 12 * 70

def random_pilot():
    pilot = Person()
    years_of_service = int('2024') - int(pilot.empDate[:4])

    f_hours = years_of_service * FLIGHT_HOURS_YEARLY_AVERAGE - randint(10, 100) * years_of_service
    pWage = pilot_wage(f_hours)
    sql = f'INSERT INTO pilot ("emp_id", "first_name", "last_name", "wage", "dob", "address", "hire_date", "flight_hours") VALUES ({pilot.empId}, \'{pilot.first_name}\', \'{pilot.last_name}\', {pWage}, \'{pilot.birthdate}\', \'{pilot.address}\', \'{pilot.empDate}\', \'{f_hours}\');'
    return sql


def random_attendant():
    attendant = Person()
    sql = f'INSERT INTO attendant ("emp_id", "first_name", "last_name", "wage", "dob", "address", "hire_date") VALUES ({attendant.empId}, \'{attendant.first_name}\', \'{attendant.last_name}\', {attendant.get_wage(2000, 4000)}, \'{attendant.birthdate}\', \'{attendant.address}\', \'{attendant.empDate}\');'
    return sql


def random_medic():
    medic = Person()
    field = choice(rand_data.medical_field)
    sql = f'INSERT INTO medic ("emp_id", "first_name", "last_name", "wage", "dob", "address", "hire_date", "field") VALUES ({medic.empId}, \'{medic.first_name}\', \'{medic.last_name}\', {medic.get_wage(4000, 6000)}, \'{medic.birthdate}\', \'{medic.address}\', \'{medic.empDate}\', \'{field}\');'
    return sql


def random_ground_crew():
    crew = Person()
    field = choice(rand_data.crew_type)
    sql = f'INSERT INTO ground_crew ("emp_id", "first_name", "last_name", "wage", "dob", "address", "hire_date", "type") VALUES ({crew.empId}, \'{crew.first_name}\', \'{crew.last_name}\', {crew.get_wage(2000, 4500)}, \'{crew.birthdate}\', \'{crew.address}\', \'{crew.empDate}\', \'{field}\');'
    return sql


def buildCarouselAircraft():
    with open('../init_sql/carousel_aircraft.sql', 'w') as f:
        for i in range(len(rand_data.FLEET)):
            try:
                f.write(random_carousel_aircraft() + '\n')
            except:
                i -= 1
                print('error in luggage', i)
    print("Luggage generated successfully")


def buildLuggage():
    with open('../init_sql/luggage.sql', 'w') as f:
        for i in range(170_000):
            try:
                f.write(random_luggage() + '\n')
            except:
                i -= 1
                print('error in luggage', i)
    print("Luggage generated successfully")


def buildCarousel():
    with open('../init_sql/carousel.sql', 'w') as f:
        for i in range(3_000):
            try:
                f.write(random_carousel() + '\n')
            except:
                i -= 1
                print('error in carousel', i)
    print("Carousel generated successfully")


def buildPilot():
    with open('../init_sql/pilot.sql', 'w') as f:
        for i in range(4000):
            try:
                f.write(random_pilot() + '\n')
            except:
                i -= 1
                print('error in pilot', i)
    print("Pilot generated successfully")


def buildAttendant():
    with open('../init_sql/attendant.sql', 'w') as f:
        for i in range(2000):
            try:
                f.write(random_attendant() + '\n')
            except:
                i -= 1
                print('error in attendant', i)
    print("Attendant generated successfully")


def buildMedic():
    with open('../init_sql/medic.sql', 'w') as f:
        for i in range(500):
            try:
                f.write(random_medic() + '\n')
            except:
                i -= 1
                print('error in medic', i)
    print("Medic generated successfully")


def buildGroundCrew():
    with open('../init_sql/ground_crew.sql', 'w') as f:
        for i in range(2000):
            try:
                f.write(random_ground_crew() + '\n')
            except:
                i -= 1
                print('error in ground_crew', i)
    print("Ground Crew generated successfully")

#buildCarouselAircraft()
#buildCarousel()
#buildLuggage()
buildPilot()
#buildAttendant()
#buildMedic()
#buildGroundCrew()
