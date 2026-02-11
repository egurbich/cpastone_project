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

        stats = {}

        stats['total_trips'] = len(self.trips)

        stats['avg_distance'] = self.trips['distance_km'].mean()

        popular_station_id = self.trips['start_station_id'].mode()[0]
        stats['popular_station'] = self.stations[self.stations['station_id'] == popular_station_id]['station_name'].values[0]

        stats['peak_hour'] = self.trips['start_time'].dt.hour.mode()[0]

        stats['bike_type_dist'] = self.trips['bike_type'].value_counts(normalize=True) * 100

        stats['total_maint_cost'] = self.maintenance['cost'].sum()

        if 'battery_level' in self.trips.columns:
             stats['avg_battery'] = self.trips[self.trips['bike_type'] == 'electric']['battery_level'].mean()

        return stats
    