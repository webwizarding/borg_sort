# Algorithm examples 

---

These files **DO NOT** use the library/wrapper to sort the datasets.

They are examples of sorting kaggle datasets and randomized numbers as datasets with the original implimentations of the algorithm.

From testing (in this github and not) it shows that my algorithm comes a bit slower to popular algorithms for larger datasets but can win the race in smaller datasets.

---

## Performance

### SydneyHousePrices
```

Borg Sort Progress: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  3.35it/s]
Borg Sort Time: 0.32851624488830566 seconds

QuickSort Progress: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.65it/s]
QuickSort Time: 0.13396215438842773 seconds
```

## kc_house_data
```
Borg Sort Progress: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 29.82it/s]
Borg Sort Time: 0.0492401123046875 seconds

QuickSort Progress: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 75.70it/s]
QuickSort Time: 0.026501893997192383 seconds
```

## algo.cpp
This file is just testing the implimentation of the sorting algorithm in a different coding language to see the difference in performance.
Test this out yourself as right now it just uses randomized numbers and most likely does not display stable performance output.

---
