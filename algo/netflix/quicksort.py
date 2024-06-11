import time
import pandas as pd
from tqdm import tqdm

def quicksort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

file_path = 'Netflix Userbase.csv'
data = pd.read_csv(file_path)

print("Column names in the CSV file:", data.columns)

ages = data['Age'].tolist()
genders = data['Gender'].tolist()

start_time = time.time()
quicksort(ages, 0, len(ages) - 1)
quicksort_time = time.time() - start_time

print(f"QuickSort Time: {quicksort_time} seconds")

sorted_genders = [x for _, x in sorted(zip(data['Age'].tolist(), genders))]

sorted_data = pd.DataFrame({'Age': ages, 'Gender': sorted_genders})
sorted_data.to_csv('sorted_ages.csv', index=False)
