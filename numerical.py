import numpy as np

class NumericalProcessor:

    @staticmethod
    def calculate_euclidean_distance(lat1, lon1, lat2, lon2):

        p1 = np.array([lat1, lon1])
        p2 = np.array([lat2, lon2])
        distance = np.sqrt(np.sum(np.square(p1 - p2)))
        return distance

    @staticmethod
    def calculate_descriptive_stats(data_series):

        arr = np.array(data_series)
        
        stats = {
            "mean": np.mean(arr),
            "median": np.median(arr),
            "std_dev": np.std(arr),
            "max": np.max(arr),
            "min": np.min(arr)
        }
        return stats

if __name__ == "__main__":
    
    proc = NumericalProcessor()
    
    dist = proc.calculate_euclidean_distance(0, 0, 3, 4)
    print(f"Test Distance: {dist}")