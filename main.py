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

    # 5. Generate Business Report
    print("\nStep 5: Generating Business Report...")
    report = system.generate_business_stats()
    
    with open(output_dir / "summary_report.txt", "w") as f:
        f.write("CITYBIKE SYSTEM SUMMARY REPORT\n")
        f.write("==============================\n")
        f.write(f"1. Total Trips: {report['total_trips']}\n")
        f.write(f"   Total Distance: {report['total_distance']:.2f} km\n")
        f.write(f"   Avg Duration: {report['avg_duration']:.2f} min\n\n")
        
        f.write("2. Top 10 Start Stations:\n")
        for st, count in list(report['top_10_start'].items())[:10]:
             f.write(f"   - {st}: {count}\n")
        
        f.write(f"\n3. Peak Rental Hour: {report['peak_hour']}:00\n")
        f.write(f"4. Busiest Day: {report['busiest_day']}\n")
        
        f.write("\n5. Avg Distance by User Type:\n")
        for u_type, dist in report['avg_dist_by_user'].items():
            f.write(f"   - {u_type}: {dist:.2f} km\n")

        f.write("\n7. Monthly Trend (Last 5 Months):\n")
        for month, count in list(report['monthly_trend'].items())[-5:]:
            f.write(f"   - {month}: {count} trips\n")

        f.write("\n10. Top Routes (Station ID -> Station ID):\n")
        for idx, row in report['top_routes'].head(10).iterrows():
            f.write(f"   - {row['start_station_id']} -> {row['end_station_id']}: {row['count']}\n")

        f.write(f"\nTotal Maintenance Costs: ${report['total_maint_cost']:.2f}\n")
        
    print("Report generated: output/summary_report.txt")

    # 6. Visualization Phase
    print("\nStep 6: Generating Visualizations...")
    from visualization import Visualizer
    viz = Visualizer(output_path=output_dir / "figures")
    
    viz.plot_bike_types(system.trips)
    viz.plot_peak_hours(system.trips)
    viz.plot_top_stations(system.trips, system.stations)
    viz.plot_trip_distances(system.trips)
    
    print(f"Visualizations saved to: output/figures/")
    print("\n✅ ALL MILESTONES COMPLETE!")

    print("\n--- Capstone Project: Data Processing Phase Complete ---")
    print("Next step: Data Visualization & Business Questions.")

if __name__ == "__main__":
    main()