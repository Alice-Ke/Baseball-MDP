import numpy as np
import pandas as pd
import bellman as mdp

# P = np.array([
# [
# 	[0, 3/4, 1/4, 0],
# 	[0, 1, 0, 0],
# 	[0, 0, 1, 0],
# 	[0, 0, 0, 1]

# ],
# [
# 	[0, 0, 2/3, 1/3],
# 	[0, 1, 0, 0],
# 	[0, 0, 1, 0],
# 	[0, 0, 0, 1]
# ]
# ])

# R = np.array([
# [ 3/4, 2/3 ],
# [0, 0],
# [0, 0],
# [0, 0]
# ])

# oR = np.zeros((2, 4, 4))

# # stand
# oR[0, 0, 1] = 1;

# # swing
# oR[1, 0, 3] = 2;

# p = np.zeros((2, 4, 4))
# p[0, 0, 1] = 3
# p[0, 0, 2] = 1
# p[1, 0, 2] = 2
# p[1, 0, 3] = 1

# sumP = np.sum( p, axis=2 ).reshape(2, 4, 1)
# index_zero_P = np.argwhere(sumP == 0)
# sumP[sumP==0] = 1
# # print(index_zero_P)
# P = np.array( p / sumP )
# for arr in index_zero_P:
#   P[ arr[0], arr[1], arr[1] ] = 1
# print(P)

# # -------------------R
# R = np.zeros((2, 4))
# for aa in range(2):
#   R[aa] = np.sum( np.multiply( P[aa], oR[aa]) , 1 )
# R = R.transpose()

P = np.array([
[
	[1, 0, 0, 0],
	[1/2, 0, 0, 1/2],
	[1/2, 0, 1/2, 0],
	[0, 0, 1/2, 1/2]

],
[
	[1/2, 1/2, 0, 0],
	[0, 1, 0, 0],
	[1/2, 1/2, 0, 0],
	[0, 1, 0, 0]
]
])


R = np.zeros((2, 4, 4))
for i in range(4):
	for j in range(2):
		R[j, i, 3] = 10
		R[j, i, 2] = 10

vi = mdp.value_iteration(P, R, 0.9, 2.22 * 10 ** (-16), 3, 4, 2)

print(vi[0])
print(vi[1])