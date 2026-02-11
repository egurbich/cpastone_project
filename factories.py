from models import ClassicBike, ElectricBike, Station, Trip, CasualUser, MemberUser

class BikeFactory:
    @staticmethod
    def create_bike(data: dict):
        """
        Creates a Bike object based on the bike_type in data.
        'data' is a dictionary representing a row from CSV.
        """
        if (data['bike_type'] == 'electric'):
            return ElectricBike(
                bike_id=data['bike_id'],
                bike_type=data['bike_type'],
                battery_level=data['battery_level'],
                max_range_km=data['max_range_km']
            )
        else:
            return ClassicBike(
                bike_id=data['bike_id'],
                bike_type=data['bike_type'],
                gear_count=data['gear_count']
            )

class UserFactory:
    @staticmethod
    def create_user(data: dict):
        if (data['user_type'] == 'casual'):
            return CasualUser(
                user_id=data['user_id'],
                name=data['name'],
                email=data['email'],
                user_type=data['user_type'],
                day_pass_count=data['day_pass_count']
            )
        else:
            return MemberUser(
                user_id=data['user_id'],
                name=data['name'],
                email=data['email'],
                user_type=data['user_type'],
                membership_start=data['membership_start'],
                membership_end=data['membership_end'],
                tier=data['tier']
            )
        

class TripFactory:
    @staticmethod
    def create_trip(data: dict):
        return Trip(data)
    
class StationFactory:
    @staticmethod
    def create_station(data: dict):
        return Station(
            entity_id=data['station_id'],
            name=data['name'],
            capacity=data['capacity'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )