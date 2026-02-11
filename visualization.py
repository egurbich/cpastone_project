import matplotlib.pyplot as plt
from pathlib import Path

class Visualizer:
    """
    Handles data visualization using Matplotlib.
    Generates and saves charts to the output directory.
    """
    
    def __init__(self, output_path="output/figures"):
        self.output_path = Path(output_path)
        # Create directory if it doesn't exist
        self.output_path.mkdir(parents=True, exist_ok=True)

    def plot_bike_types(self, trips_df):
        """1. Pie chart of bike types (Classic vs Electric)"""
        plt.figure(figsize=(8, 6))
        trips_df['bike_type'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['skyblue', 'orange'])
        plt.title('Distribution of Bike Types')
        plt.ylabel('')
        plt.savefig(self.output_path / "bike_types_dist.png")
        plt.close()

    def plot_peak_hours(self, trips_df):
        """2. Bar chart of rentals per hour"""
        plt.figure(figsize=(10, 6))
        trips_df['start_time'].dt.hour.value_counts().sort_index().plot(kind='bar', color='green')
        plt.title('Peak Rental Hours')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Trips')
        plt.savefig(f"{self.output_path}/peak_hours.png")
        plt.close()

    def plot_top_stations(self, trips_df, stations_df):
        """3. Horizontal bar chart of Top 10 Stations"""
        plt.figure(figsize=(10, 8))
        top_stations = trips_df['start_station_id'].value_counts().head(10)
        # Map IDs to names for the chart
        names = [stations_df[stations_df['station_id'] == sid]['station_name'].values[0] for sid in top_stations.index]
        
        plt.barh(names, top_stations.values, color='purple')
        plt.title('Top 10 Most Popular Start Stations')
        plt.xlabel('Number of Trips')
        plt.gca().invert_yaxis() # Highest on top
        plt.savefig(f"{self.output_path}/top_stations.png")
        plt.close()

    def plot_trip_distances(self, trips_df):
        """4. Box plot of trip distances to see outliers"""
        plt.figure(figsize=(8, 6))
        plt.boxplot(trips_df['distance_km'])
        plt.title('Trip Distance Distribution')
        plt.ylabel('Distance (km)')
        plt.savefig(f"{self.output_path}/distance_boxplot.png")
        plt.close()