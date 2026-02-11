from datetime import datetime
from abc import ABC, abstractmethod

class Entity(ABC):
    """Abstract base class for all system entities.
        Ensures that every object has a unique ID and a creation timestamp."""   
     
    def __init__(self, entity_id: int):
        self.id = entity_id
        self.created_at = datetime.now()
    
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass    

class Bike(Entity):
    """Base class representing a bicycle in the system."""

    status = ("available", "in_use", "maintenance")

    def __init__(self, bike_id: int, bike_type: str):
        super().__init__(bike_id)
        self.bike_type = bike_type

    def __str__(self):
        return f"Bike {self.id} ({self.bike_type})"
    
    def __repr__(self):
        return f"Bike(id={self.id}, type={self.bike_type})"
    
class ClassicBike(Bike):
    """A standard bicycle with mechanical gears."""

    def __init__(self, bike_id, bike_type, gear_count: int):
        super().__init__(bike_id, bike_type)
        self.gear_count = gear_count

    def __str__(self):
        return super().__str__()

class ElectricBike(Bike):
    """An electric bicycle with an integrated battery and power assistance."""

    def __init__(self, bike_id, bike_type, battery_level: int, max_range_km: float):
        super().__init__(bike_id, bike_type)
        self.battery_level = battery_level
        self.max_range_km = max_range_km

    def __str__(self):
        return super().__str__()

class Station(Entity):
    """A physical location where users can pick up or return bikes."""

    def __init__(self, entity_id: int, name: str, capacity: int, latitude: float, longitude: float):
        super().__init__(entity_id)
        self.station_id = entity_id
        self.name = name
        self.capacity = capacity
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"Station '{self.name}' (ID: {self.id}) - Cap: {self.capacity}"

    def __repr__(self):
        return f"Station(id={self.id}, name='{self.name}', capacity={self.capacity})"

class User(Entity):
    """Base class for all system users."""

    def __init__(self, entity_id: int, name: str, email: str, user_type: str):
        super().__init__(entity_id)
        self.user_id = entity_id
        self.name = name
        self.email = email
        self.user_type = user_type

    def __str__(self):
        return f"User: {self.name} ({self.user_type})"

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', type='{self.user_type}')"

class CasualUser(User):
    """A user without a long-term subscription, typically using day passes."""

    def __init__(self, entity_id, name, email, user_type, day_pass_count: int):
        super().__init__(entity_id, name, email, user_type)
        self.day_pass_count = day_pass_count

    def __str__(self):
        return super().__str__() + f" (Passes: {self.day_pass_count})"

    def __repr__(self):
        return f"CasualUser(id={self.id}, name='{self.name}', passes={self.day_pass_count})"

class MemberUser(User):
    """A registered user with an active subscription plan (Basic or Premium)."""

    tier = ("basic", "premium")
    
    def __init__(
            self, 
            entity_id, 
            name, 
            email, 
            user_type, 
            membership_start: str, 
            membership_end: str, 
            tier: str):
        super().__init__(entity_id, name, email, user_type)
        self.membership_start = membership_start
        self.membership_end = membership_end
        self.tier = tier

    def __str__(self):
        return super().__str__() + f" [Tier: {self.tier}]"

    def __repr__(self):
        return f"MemberUser(id={self.id}, name='{self.name}', tier='{self.tier}')"

class Trip(Entity):
    """Record of a single bike rental, connecting a user, a bike, and two stations."""

    def __init__(
            self, 
            entity_id: int, 
            user: User, 
            bike: Bike, 
            start_station: Station, 
            end_station: Station,
            start_time: str,
            end_time: str,
            distance_km: float):
        super().__init__(entity_id)
        self.trip_id = entity_id
        self.user = user
        self.bike = bike
        self.start_station = start_station
        self.end_station = end_station
        self.start_time = start_time
        self.end_time = end_time
        self.distance_km = distance_km

    def __str__(self):
        return f"Trip {self.id}: Bike {self.bike.id} from {self.start_station.name} to {self.end_station.name}"

    def __repr__(self):
        return f"Trip(id={self.id}, user_id={self.user.id}, bike_id={self.bike.id}, dist={self.distance_km}km)"

class MaintenanceRecord(Entity):
    """Log of maintenance, repairs, or diagnostics performed on a specific bike."""

    def __init__(
            self,
            entity_id: int,
            bike: Bike,
            date: str,
            maintenance_type: str,
            cost: float,
            description: str):
        super().__init__(entity_id)
        self.record_id = entity_id
        self.bike = bike
        self.date = date
        self.maintenance_type = maintenance_type
        self.cost = cost
        self.description = description

    def __str__(self):
        # Виводимо дату, ID велосипеда, тип робіт та вартість
        return f"Maintenance [{self.date}] | Bike {self.bike.id} | {self.maintenance_type} | Cost: ${self.cost:.2f}"

    def __repr__(self):
        # Технічне представлення для дебагу
        return (f"MaintenanceRecord(id={self.id}, bike_id={self.bike.id}, "
                f"type='{self.maintenance_type}', cost={self.cost})")

class BikeShareSystem(Entity):
    """The main system orchestrator that manages data processing and operations."""

    def __init__(self, entity_id: int):
        super().__init__(entity_id)

    def __str__(self):
        return f"CityBike System Manager (Active)"

    def __repr__(self):
        return "BikeShareSystem()"
