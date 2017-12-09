import numpy as np



def getSpan( array ):
	return array.max() - array.min()


def _bellmanOperator(P, R, discount, V, s, a):
		Q = np.empty((a, s))
		# V = np.concatenate(( V, np.zeros((6)) ), axis = 0 )
		for aa in range(a):
			# print( np.multiply( P[aa], R[aa] ).shape )
			Q[aa] = np.sum( np.multiply( P[aa], R[aa] ) , 1 ) + discount * np.dot( ( P[aa][ :, 0:12 ] ), V )
		# Get the policy and value, for now it is being returned but...
		# Which way is better?
		# 1. Return, (policy, value)
		return (Q.argmax(axis=0), Q.max(axis=0))


def value_iteration( P, R, discount, thresh, max_iter, s, a ):
	iteration = 0
	V = np.zeros((s))
	while True:
		iteration += 1
		Vprev = V
		# Bellman Operator: compute policy and value functions
		policy, V = _bellmanOperator(P, R, discount, Vprev, s, a)
		variation = getSpan(V - Vprev)
		# print(variation)

		if thresh is not None and variation < thresh:
			# print("min thresh")
			break
		elif iteration == max_iter:
			# print("max iteration")
			break
	return( policy, V )

def policy_evaluation( P, R, V, discount, thresh, max_iter, s, a ):
		policy_P = np.zeros((s, 18))
		policy_R = np.zeros((s, 18))
		for i in range(s):
			policy_P[i] = P[V[i]][i]
		for i in range(s):
			policy_R[i] = R[V[i]][i]

		V = np.zeros((s))
		iteration = 0
		while True:
			iteration += 1
			Vprev = V
			V = np.sum( np.multiply( policy_P, policy_R ) , 1 ) + discount * np.dot( policy_P[:, 0:12] ,Vprev)
			variation = getSpan(V - Vprev)
			if thresh is not None and variation < thresh:
				# print("min thresh")
				break
			elif iteration == max_iter:
				# print("max iteration")
				break
		return V

if __name__ == "__main__":
	V = np.ones((18))
	V = np.concatenate(( V, np.zeros((6)) ), axis = 0 )
	print(V)



