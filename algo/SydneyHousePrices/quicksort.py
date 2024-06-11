import time
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

file_path = 'SydneyHousePrices.csv'
data = pd.read_csv(file_path)

prices = data['sellPrice'].tolist()

start_time = time.time()
for _ in tqdm(range(1), desc="QuickSort Progress"):
    quicksort_sorted = quicksort(prices.copy())
quicksort_time = time.time() - start_time

print(f"QuickSort Time: {quicksort_time} seconds")

methods = ['QuickSort']
times = [quicksort_time]

plt.bar(methods, times, color=['blue'])
plt.xlabel('Sorting Method')
plt.ylabel('Time (seconds)')
plt.title('Sorting Time Comparison')
plt.show()

sorted_data = data.copy()
sorted_data['sellPrice'] = quicksort_sorted
sorted_data.to_csv('quicksort_sorted_sellprices.csv', index=False)
