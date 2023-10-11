"""
Credits:
https://www.tutorialspoint.com/data_structures_algorithms/binary_search_algorithm.htm
https://www.geeksforgeeks.org/python-program-for-binary-search/
"""

def binary_search(arr, low, high, x):
   # Check for the base case
   if high >= low:

      mid = (high + low) // 2

      # If element is already at the middle:
      if arr[mid] == x:
         return mid

      # If element is smaller than mid, then it can only be present in the left subarray
      elif arr[mid] > x:
         return binary_search(arr, low, mid - 1, x)

      # Else the element can only be present in the right subarray
      else:
         return binary_search(arr, mid + 1, high, x)

   else:
      # Element is not present in the array
      return -1


# Test array
arr = [1, 3, 6, 10, 15]
x = 10

# Function call
result = binary_search(arr, 0, len(arr) - 1, x)

if result != -1:
   print("Element is present at index", str(result))
else:
   print("Element is not present in array")
