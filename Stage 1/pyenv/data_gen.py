import rand_data
import random


def air_reg_code():
    if len(rand_data.FLEET) == 0:
        return None
    return rand_data.FLEET[random.randint(0, len(rand_data.FLEET) - 1)]


def weights():
    global iata_weights
    iata_weights = [1] * len(rand_data.IATAs)
    iata_weights[0] = 12
    for i in range(1, 10):
        iata_weights[i] = 10
    for i in range(10, 20):
        iata_weights[i] = 9


# pairs of <aircraft_rn, iata>
aircraft_iata_dict = {}


def get_iata():
    return random.choices(rand_data.IATAs, iata_weights, k=1)[0]


class Carousel:
    count = 1

    def __init__(self) -> None:
        self.id = self.count
        Carousel.count += random.randint(1, 30)
        self.iata = get_iata()
        self.capacity = random.randint(800, 3000)
        self.terminal = random.randint(1, 10)


carousels = []


def carousel():
    # Carousel with no incoming planes
    c = Carousel()
    carousels.append(c)
    return c.id, c.iata, c.capacity, c.terminal


def assign_aircraft(aircraft_rn):
    # p = 20% [get an existing carousel]
    if random.randint(0, 100) <= 20:
        c = carousels[random.randint(0, len(carousels) - 1)]
    # p = 80% [create a new carousel]
    else:
        c = Carousel()
        carousels.append(c)

    return c.id, aircraft_rn
