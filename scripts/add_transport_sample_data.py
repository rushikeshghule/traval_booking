import sys
import os
import random
import datetime
from decimal import Decimal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_booking.settings')
import django
django.setup()

# Flight imports
from flight.models import Airline, Airport, Flight, FlightSeat
# Bus imports
from bus.models import BusOperator, BusRoute, Bus, BusSchedule, BusSeat
# Train imports
from train.models import TrainOperator, Station, Train, TrainRoute, TrainClass

def create_airlines(num=5):
    airlines = []
    for i in range(1, num+1):
        airline = Airline.objects.create(
            name=f"Airline {i}",
            code=f"AL{i:02}",
            description=f"Sample airline {i}",
        )
        airlines.append(airline)
    return airlines

def create_airports(num=10):
    airports = []
    for i in range(1, num+1):
        airport = Airport.objects.create(
            name=f"Airport {i}",
            code=f"AP{i:03}",
            city=f"City{i}",
            country="India",
        )
        airports.append(airport)
    return airports

def create_flights(airlines, airports, num=20):
    flights = []
    for i in range(num):
        airline = random.choice(airlines)
        src, dst = random.sample(airports, 2)
        dep = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30), hours=random.randint(0, 23))
        arr = dep + datetime.timedelta(hours=random.randint(1, 5))
        flight = Flight.objects.create(
            airline=airline,
            flight_number=f"F{i:04}",
            source=src,
            destination=dst,
            departure_time=dep,
            arrival_time=arr,
            duration=arr-dep,
            flight_type='domestic',
            base_price=Decimal(random.randint(2000, 8000)),
            available_seats=60,
            aircraft_type='Boeing 737',
        )
        flights.append(flight)
    return flights

def create_flight_seats(flights):
    for flight in flights:
        for i in range(1, 61):
            FlightSeat.objects.create(
                flight=flight,
                seat_number=f"{i}",
                seat_class='economy',
                price=flight.base_price,
            )

def create_bus_operators(num=5):
    ops = []
    for i in range(1, num+1):
        op = BusOperator.objects.create(
            name=f"BusOperator {i}",
            description=f"Sample bus operator {i}",
        )
        ops.append(op)
    return ops

def create_bus_routes(num=10):
    routes = []
    for i in range(1, num+1):
        src = f"City{i}"
        dst = f"City{(i%10)+1}"
        route = BusRoute.objects.create(
            source=src,
            destination=dst,
            distance=Decimal(random.randint(100, 1000)),
            duration=datetime.timedelta(hours=random.randint(2, 12)),
        )
        routes.append(route)
    return routes

def create_buses(operators, num=10):
    buses = []
    for i in range(num):
        op = random.choice(operators)
        bus = Bus.objects.create(
            operator=op,
            bus_number=f"BUS{i:03}",
            bus_type='ac',
            total_seats=40,
            amenities='WiFi, AC',
        )
        buses.append(bus)
    return buses

def create_bus_schedules(buses, routes, num=20):
    schedules = []
    for i in range(num):
        bus = random.choice(buses)
        route = random.choice(routes)
        dep = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 20), hours=random.randint(0, 23))
        arr = dep + datetime.timedelta(hours=random.randint(2, 12))
        sch = BusSchedule.objects.create(
            bus=bus,
            route=route,
            departure_time=dep,
            arrival_time=arr,
            fare=Decimal(random.randint(300, 1200)),
            available_seats=40,
        )
        schedules.append(sch)
    return schedules

def create_bus_seats(schedules):
    for sch in schedules:
        for i in range(1, 41):
            BusSeat.objects.create(
                schedule=sch,
                seat_number=f"{i}",
                seat_type='window' if i%4==1 else 'aisle',
            )

def create_train_operators(num=3):
    ops = []
    for i in range(1, num+1):
        op = TrainOperator.objects.create(
            name=f"TrainOperator {i}",
            description=f"Sample train operator {i}",
        )
        ops.append(op)
    return ops

def create_stations(num=10):
    stations = []
    for i in range(1, num+1):
        st = Station.objects.create(
            name=f"Station {i}",
            code=f"ST{i:03}",
            city=f"City{i}",
            state=f"State{i%5}",
        )
        stations.append(st)
    return stations

def create_trains(operators, num=6):
    trains = []
    for i in range(num):
        op = random.choice(operators)
        train = Train.objects.create(
            operator=op,
            train_number=f"TRN{i:03}",
            name=f"Train {i}",
            train_type='express',
        )
        trains.append(train)
    return trains

def create_train_routes(trains, stations, num=12):
    routes = []
    for i in range(num):
        train = random.choice(trains)
        src, dst = random.sample(stations, 2)
        dep = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30), hours=random.randint(0, 23))
        arr = dep + datetime.timedelta(hours=random.randint(4, 20))
        route = TrainRoute.objects.create(
            train=train,
            source=src,
            destination=dst,
            distance=Decimal(random.randint(200, 2000)),
            duration=arr-dep,
            departure_time=dep,
            arrival_time=arr,
        )
        routes.append(route)
    return routes

def create_train_classes(routes):
    class_types = ['SL', '3A', '2A', '1A', 'CC']
    for route in routes:
        for ct in class_types:
            TrainClass.objects.create(
                train_route=route,
                class_type=ct,
                fare=Decimal(random.randint(400, 2000)),
                available_seats=100,
            )

def main():
    airlines = create_airlines()
    airports = create_airports()
    flights = create_flights(airlines, airports)
    create_flight_seats(flights)

    bus_ops = create_bus_operators()
    bus_routes = create_bus_routes()
    buses = create_buses(bus_ops)
    bus_schedules = create_bus_schedules(buses, bus_routes)
    create_bus_seats(bus_schedules)

    train_ops = create_train_operators()
    stations = create_stations()
    trains = create_trains(train_ops)
    train_routes = create_train_routes(trains, stations)
    create_train_classes(train_routes)

if __name__ == '__main__':
    main()
