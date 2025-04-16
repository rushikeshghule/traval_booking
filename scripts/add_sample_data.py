import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_booking.settings')
import django
django.setup()

from hotel.models import Hotel, RoomType, Room

def create_hotels():
    # Create sample hotels
    hotel1 = Hotel.objects.create(
        name='Seaside Resort',
        address='123 Beach Road',
        city='Goa',
        state='Goa',
        country='India',
        postal_code='403001',
        star_rating=5,
        description='A luxury resort by the sea.',
        amenities='Pool, Spa, WiFi, Parking',
    )
    hotel2 = Hotel.objects.create(
        name='Mountain Inn',
        address='456 Hilltop Ave',
        city='Manali',
        state='Himachal Pradesh',
        country='India',
        postal_code='175131',
        star_rating=4,
        description='A cozy inn in the mountains.',
        amenities='WiFi, Parking, Breakfast',
    )
    print(f"Created hotels: {hotel1}, {hotel2}")
    return [hotel1, hotel2]

def create_room_types(hotel):
    # Create room types for a hotel
    deluxe = RoomType.objects.create(
        hotel=hotel,
        name='Deluxe Room',
        room_type='deluxe',
        description='Spacious room with sea/mountain view.',
        price_per_night=5000,
        capacity=2,
        amenities='AC, TV, Mini Bar',
        size='35 sqm',
    )
    suite = RoomType.objects.create(
        hotel=hotel,
        name='Suite',
        room_type='suite',
        description='Luxury suite with living area.',
        price_per_night=9000,
        capacity=4,
        amenities='AC, TV, Mini Bar, Living Room',
        size='60 sqm',
    )
    print(f"Created room types for {hotel.name}: {deluxe}, {suite}")
    return [deluxe, suite]

def create_rooms(hotel, room_types):
    # Create rooms for each room type
    for rt in room_types:
        for i in range(1, 4):
            room = Room.objects.create(
                hotel=hotel,
                room_type=rt,
                room_number=f"{rt.name[:2].upper()}{i}",
                floor=str(i),
                status='available',
            )
            print(f"Created room: {room}")

def main():
    hotels = create_hotels()
    for hotel in hotels:
        room_types = create_room_types(hotel)
        create_rooms(hotel, room_types)

if __name__ == '__main__':
    main()
