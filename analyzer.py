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

        # 1. First fill numeric columns with 0
        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)

        # if there other empty cells - set there Unknown
        object_cols = df.select_dtypes(include=['object']).columns
        df[object_cols] = df[object_cols].fillna('Unknown')

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
        # Assumes 'duration_minutes' exists or calculates it
        if 'duration_minutes' not in self.trips.columns:
            self.trips['duration_minutes'] = (self.trips['end_time'] - self.trips['start_time']).dt.total_seconds() / 60
        stats['avg_duration'] = self.trips['duration_minutes'].mean()

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

        # 6. Bike Utilization Rate
        # Formula: (Total Minutes Ridden) / (Total Fleet Minutes Available)
        # Total Fleet Minutes = (Number of unique bikes) * (Time range of dataset in minutes)
        if not self.trips.empty and 'duration_minutes' in self.trips.columns:
            total_trip_minutes = self.trips['duration_minutes'].sum()
            unique_bikes_count = self.trips['bike_id'].nunique()
            
            # Calculate time range of dataset
            time_range_min = (self.trips['end_time'].max() - self.trips['start_time'].min()).total_seconds() / 60
            
            # Avoid division by zero
            if time_range_min > 0 and unique_bikes_count > 0:
                 total_potential_minutes = unique_bikes_count * time_range_min
                 stats['utilization_rate'] = (total_trip_minutes / total_potential_minutes) * 100
            else:
                 stats['utilization_rate'] = 0.0
        else:
            stats['utilization_rate'] = 0.0

        # 7. Monthly trip trend
        # Extract YYYY-MM
        self.trips['month_year'] = self.trips['start_time'].dt.to_period('M')
        stats['monthly_trend'] = self.trips['month_year'].value_counts().sort_index().to_dict()

        # 8. Top 15 active users
        stats['top_users'] = self.trips['user_id'].value_counts().head(15).to_dict()

        # 9. Maintenance cost by bike type (classic vs. electric)
        # Create a mapping of bike_id -> bike_type from trips data
        bike_types_map = self.trips.set_index('bike_id')['bike_type'].to_dict()
        
        # Map bike_type to maintenance dataframe
        # Ensure maintenance has bike_id
        if 'bike_id' in self.maintenance.columns:
            self.maintenance['bike_type'] = self.maintenance['bike_id'].map(bike_types_map).fillna('Unknown')
            stats['maint_cost_by_type'] = self.maintenance.groupby('bike_type')['cost'].sum().to_dict()
        else:
            stats['maint_cost_by_type'] = {"Error": "bike_id missing in maintenance data"}
        
        stats['total_maint_cost'] = self.maintenance['cost'].sum()

        # 10. Most common routes (Start -> End)
        stats['top_routes'] = self.trips.groupby(['start_station_id', 'end_station_id']).size().nlargest(10).reset_index(name='count')
        
        # Map IDs to Names for Route using the shared helper
        stats['top_routes']['start_name'] = stats['top_routes']['start_station_id'].apply(self.get_station_name)
        stats['top_routes']['end_name'] = stats['top_routes']['end_station_id'].apply(self.get_station_name)

        # 12. Avg trips per user
        stats['avg_trips_per_user_type'] = self.trips.groupby('user_type')['user_id'].value_counts().groupby('user_type').mean().to_dict()

        return stats
    
    def get_station_name(self, station_id):
        """Helper to get a single station name from an ID"""
        name = self.stations.loc[self.stations['station_id'] == station_id, 'station_name']
        return name.values[0] if not name.empty else f"Station {station_id}"

    def _map_station_names(self, series_ids):
        """Helper to map station IDs (index) to names (keys) with counts (values)"""
        result = {}
        for sid, count in series_ids.items():
            station_label = self.get_station_name(sid)
            result[station_label] = count
        return result
    