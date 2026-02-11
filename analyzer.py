"""
Logic for getting data from all source files and write/update output files
"""

import pandas
import numpy
from pathlib import Path

SOURCE_DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DATA_DIR = Path(__file__).resolve().parent / "output"

class BikeShare:

    def __init__(self):
        # here we saving ours cleaned files data
        self.stations = None
        self.trips = None
        self.maintenance = None

    def load_and_clean_data(self, file_name):

        file_path = SOURCE_DATA_DIR / file_name
        
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_name} not found in {SOURCE_DATA_DIR}")

        # get file data
        df = pandas.read_csv(file_path)
        initial_count = len(df)

        # removing duplicates
        df = df.drop_duplicates()

        # search columns with name 'date' or 'time' and convert them to same type (datetime)
        date_columns = [col for col in df.columns if 'date' in col or 'time' in col]
        for col in date_columns:
            df[col] = pandas.to_datetime(df[col], errors='coerce')

        # fill empty cost cells with 0
        if 'cost' in df.columns:
            df['cost'] = df['cost'].fillna(0)

        if 'battery_level' in df.columns:
            # for ebikes set empty values with average values
            avg_battery = df['battery_level'].mean()
            df['battery_level'] = df['battery_level'].fillna(avg_battery)


        if 'distance_km' in df.columns:
            # set positive values in case if there negative once
            df = df[df['distance_km'] >= 0]

        # if there other empty cells - set there Unknown
        df = df.fillna('Unknown')    

        # Validation: end_time must be after start_time
        if 'start_time' in df.columns and 'end_time' in df.columns:
            # keep only records where trip duration was > 0 sec
            df = df[df['end_time'] > df['start_time']]

        print(f"File {file_name}: {initial_count} -> {len(df)} rows (Cleaned).")
        return df
    
    def initialize_system(self):
        """Loading all main system source files"""
        self.stations = self.load_and_clean_data("stations.csv")
        self.trips = self.load_and_clean_data("trips.csv")
        self.maintenance = self.load_and_clean_data("maintenance.csv")

    def generate_business_stats(self):
        """
        Analyzes the data to answer detailed business questions.
        Returns a dictionary with results.
        """
        stats = {}

        # 1. Total trips, distance, avg duration
        stats['total_trips'] = len(self.trips)
        stats['total_distance'] = self.trips['distance_km'].sum()
        stats['avg_distance'] = self.trips['distance_km'].mean()
        # Assumes 'duration_min' exists or calculates it
        if 'duration_min' not in self.trips.columns:
            self.trips['duration_min'] = (self.trips['end_time'] - self.trips['start_time']).dt.total_seconds() / 60
        stats['avg_duration'] = self.trips['duration_min'].mean()

        # 2. Top 10 Start & End Stations
        top_start = self.trips['start_station_id'].value_counts().head(10)
        top_end = self.trips['end_station_id'].value_counts().head(10)
        # Map IDs to names
        stats['top_10_start'] = self._map_station_names(top_start)
        stats['top_10_end'] = self._map_station_names(top_end)

        # 3. Peak usage hours
        stats['peak_hour'] = self.trips['start_time'].dt.hour.mode()[0]

        # 4. Day of the week with highest volume
        # day_name() returns Monday, Tuesday...
        stats['busiest_day'] = self.trips['start_time'].dt.day_name().value_counts().idxmax()

        # 5. Avg distance by user type
        stats['avg_dist_by_user'] = self.trips.groupby('user_type')['distance_km'].mean().to_dict()

        # 6 (Skip for now - complex without fleet size)

        # 7. Monthly trip trend
        # Extract YYYY-MM
        self.trips['month_year'] = self.trips['start_time'].dt.to_period('M')
        stats['monthly_trend'] = self.trips['month_year'].value_counts().sort_index().to_dict()

        # 8. Top 15 active users
        stats['top_users'] = self.trips['user_id'].value_counts().head(15).to_dict()

        # 9. Maintenance cost by bike type
        # We need to join maintenance with bikes or trips? 
        # Assuming maintenance.csv has 'bike_id' and we know bike types from trips?
        # For simplicity, let's just do total maintenance as placeholder or skip if mapping missing
        stats['total_maint_cost'] = self.maintenance['cost'].sum()

        # 10. Most common routes (Start -> End)
        stats['top_routes'] = self.trips.groupby(['start_station_id', 'end_station_id']).size().nlargest(10).reset_index(name='count')

        # 12. Avg trips per user
        stats['avg_trips_per_user_type'] = self.trips.groupby('user_type')['user_id'].value_counts().groupby('user_type').mean().to_dict()

        return stats

    def _map_station_names(self, series_ids):
        """Helper to map station IDs to names"""
        result = {}
        for sid, count in series_ids.items():
            name = self.stations.loc[self.stations['station_id'] == sid, 'station_name']
            station_label = name.values[0] if not name.empty else f"Station {sid}"
            result[station_label] = count
        return result
    