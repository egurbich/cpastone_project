class Algorithms:
    """
    Provides custom implementations of fundamental algorithms.
    """

    @staticmethod
    def merge_sort(arr, key_func=lambda x: x):
        """
        Sorts a list using the Merge Sort algorithm (Divide and Conquer).
        
        Args:
            arr (list): The list of elements to be sorted.
            key_func (callable): A function that extracts the comparison key 
                                 from each element (e.g., lambda x: x['duration']).
        
        Returns:
            list: A new sorted list.
        """
        # Base case: if list has 0 or 1 element, it is already sorted
        if len(arr) <= 1:
            return arr

        # Divide: Find the middle point
        mid = len(arr) // 2
        
        # Conquer: Recursively sort both halves
        left_half = Algorithms.merge_sort(arr[:mid], key_func)
        right_half = Algorithms.merge_sort(arr[mid:], key_func)

        # Combine: Merge the sorted halves back together
        return Algorithms._merge(left_half, right_half, key_func)

    @staticmethod
    def _merge(left, right, key_func):
        """
        Helper method to merge two sorted lists into one.
        """
        result = []
        i = j = 0

        # Compare elements from both lists and add the smaller one to result
        while i < len(left) and j < len(right):
            if key_func(left[i]) <= key_func(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        # Add remaining elements from both lists (if any)
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result

    @staticmethod
    def binary_search(arr, target, key_func=lambda x: x):
        """
        Performs a binary search for a specific target value.
        Assumes the list 'arr' is already sorted.
        """
        low = 0
        high = len(arr) - 1

        while low <= high:
            mid = (low + high) // 2
            mid_val = key_func(arr[mid])

            if mid_val == target:
                return arr[mid]
            elif mid_val < target:
                low = mid + 1
            else:
                high = mid - 1
        
        return None
    