import numpy as np

l1 = [1, 2]
l3 = [3, 4]
l2 = list()

l2.append(l1)
l2.append(l3)
arr = np.array(l2)
print(arr[1, :])
print(arr)
