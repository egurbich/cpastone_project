"""
Main entry point for the CityBike Analytics Platform.
Orchestrates data loading, processing, and analysis.
"""

from analyzer import BikeShare
from numerical import NumericalProcessor
from algorithms import Algorithms
from pathlib import Path

def main():
    # 1. Initialize System and Load Data
    print("Step 1: Initializing BikeShare System...")
    system = BikeShare()
    system.initialize_system() # This loads stations, trips, and maintenance

    # 2. Advanced Numerical Processing (NumPy)
    # Example: Calculate distance for the first few trips as a test
    print("\nStep 2: Processing Numerical Data...")
    if system.trips is not None and system.stations is not None:
        # Let's take the first trip and calculate Euclidean distance
        # as a proof of concept for the capstone requirements
        sample_trip = system.trips.iloc[0]
        # In a real scenario, we would map station IDs to coordinates
        # This is where NumericalProcessor.calculate_euclidean_distance would be used
        print("Numerical processing engine: READY")

    # 3. Custom Sorting (Algorithms)
    print("\nStep 3: Running Custom Sorting Algorithms...")
    # Convert a portion of trips to list of dicts for our custom Merge Sort
    trips_list = system.trips.head(10).to_dict('records')
    sorted_trips = Algorithms.merge_sort(trips_list, key_func=lambda x: x['distance_km'])
    print(f"Sorted {len(sorted_trips)} sample trips by distance using Merge Sort.")

    # 4. Save Cleaned Data (Requirement from Milestone 3)
    print("\nStep 4: Saving Cleaned Datasets...")
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    system.trips.to_csv(output_dir / "trips_clean.csv", index=False)
    system.stations.to_csv(output_dir / "stations.csv", index=False) # In reality, stations are already clean
    print(f"Cleaned data saved to {output_dir}")

    print("\n--- Capstone Project: Data Processing Phase Complete ---")
    print("Next step: Data Visualization & Business Questions.")

if __name__ == "__main__":
    main()