import numpy as np

class NumericalProcessor:
    """
    Handles mathematical and statistical computations using NumPy.
    """

    @staticmethod
    def calculate_euclidean_distance(lat1, lon1, lat2, lon2):
        """
        Calculates the straight-line (Euclidean) distance between two points.
        
        Args:
            lat1, lon1: Coordinates of the first point.
            lat2, lon2: Coordinates of the second point.
            
        Returns:
            float: The computed distance.
        """
        # Convert inputs to numpy arrays to ensure we can handle bulk data if needed
        p1 = np.array([lat1, lon1])
        p2 = np.array([lat2, lon2])
        
        # Euclidean formula: sqrt((x1-x2)^2 + (y1-y2)^2)
        distance = np.sqrt(np.sum(np.square(p1 - p2)))
        return distance

    @staticmethod
    def calculate_descriptive_stats(data_series):
        """
        Computes basic statistics for a given data series using NumPy.
        
        Args:
            data_series: A list or pandas Series of numbers (e.g., trip durations).
            
        Returns:
            dict: Dictionary containing mean, median, and standard deviation.
        """
        # Ensure we are working with a numpy array
        arr = np.array(data_series)
        
        # Calculate stats
        stats = {
            "mean": np.mean(arr),
            "median": np.median(arr),
            "std_dev": np.std(arr),
            "max": np.max(arr),
            "min": np.min(arr)
        }
        return stats

# Example of how this might be used (can be removed later)
if __name__ == "__main__":
    proc = NumericalProcessor()
    # Distance between station A (0,0) and station B (3,4) should be 5.0
    dist = proc.calculate_euclidean_distance(0, 0, 3, 4)
    print(f"Test Distance: {dist}")