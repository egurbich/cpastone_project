from analyzer import BikeShare
from numerical import NumericalProcessor
from algorithms import Algorithms
from pathlib import Path

def main():
    print("Step 1: Initializing BikeShare System...")
    system = BikeShare()
    system.initialize_system()

    print("\nStep 2: Processing Numerical Data...")
    if system.trips is not None and system.stations is not None:

        sample_trip = system.trips.iloc[0]

        print("Numerical processing engine: READY")

    print("\nStep 3: Running Custom Sorting Algorithms...")

    trips_list = system.trips.head(10).to_dict('records')
    sorted_trips = Algorithms.merge_sort(trips_list, key_func=lambda x: x['distance_km'])
    print(f"Sorted {len(sorted_trips)} sample trips by distance using Merge Sort.")

    print("\nStep 4: Saving Cleaned Datasets...")
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    system.trips.to_csv(output_dir / "trips_clean.csv", index=False)
    system.stations.to_csv(output_dir / "stations.csv", index=False)
    print(f"Cleaned data saved to {output_dir}")

    print("\n--- Capstone Project: Data Processing Phase Complete ---")
    print("Next step: Data Visualization & Business Questions.")

if __name__ == "__main__":
    main()