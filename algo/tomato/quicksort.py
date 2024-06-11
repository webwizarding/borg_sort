import time
import pandas as pd
from tqdm import tqdm

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

file_path = 'Tomato.csv'
data = pd.read_csv(file_path)

print("Column names in the CSV file:", data.columns)

averages = data['Average'].tolist()
columns = data.columns.tolist()

start_time = time.time()
for _ in tqdm(range(1), desc="QuickSort Progress"):
    sorted_averages = quicksort(averages.copy())
quicksort_time = time.time() - start_time

print(f"QuickSort Time: {quicksort_time} seconds")

sorted_indices = sorted(range(len(averages)), key=lambda k: averages[k])
sorted_data = data.iloc[sorted_indices].reset_index(drop=True)

sorted_data.to_csv('Sorted_Tomato_QuickSort.csv', index=False)
