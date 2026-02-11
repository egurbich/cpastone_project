class Algorithms:

    @staticmethod
    def merge_sort(arr, key_func=lambda x: x):

        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        
        left_half = Algorithms.merge_sort(arr[:mid], key_func)
        right_half = Algorithms.merge_sort(arr[mid:], key_func)

        return Algorithms._merge(left_half, right_half, key_func)

    @staticmethod
    def _merge(left, right, key_func):

        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if key_func(left[i]) <= key_func(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        
        return result

    @staticmethod
    def binary_search(arr, target, key_func=lambda x: x):

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

# if __name__ == "__main__":
#     test_data = [
#         {"id": 1, "duration": 45},
#         {"id": 2, "duration": 10},
#         {"id": 3, "duration": 30}
#     ]

#     sorted_data = Algorithms.merge_sort(test_data, key_func=lambda x: x['duration'])
#     print("Sorted by duration:", sorted_data)