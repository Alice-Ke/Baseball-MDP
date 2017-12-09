import os
import process
import numpy as np
import pandas as pd
import bellman as mdp
import collections

elites = [ "Halladay,Roy", 
	"Lee,Cliff", 
	"Hamels,Cole", 
	"Lester,Jon", 
	"Greinke,Zack", 
	"Lincecum,Tim", 
	"Sabathia,CC", 
	"Santana,Johan", 
	"Hernandez,Felix", 
	"Billingsley,Chad", 
	"Weaver,Jered", 
	"Kershaw,Clayton ", 
	"Carpenter,Chris", 
	"Garza,Matt", 
	"Wainwright,Adam", 
	"Jimenez,Ubaldo", 
	"Cain,Matt", 
	"Sanchez,Jonathan", 
	"Oswalt,Roy",
	"Verlander,Justin", 
	"Johnson,Josh", 
	"Danks,John", 
	"Jackson,Edwin", 
	"Scherzer,Max", 
	"Lilly,Ted"]

R = np.zeros((2, 18, 18))
for i in range(12):
	R[1, i, 13] = 2
	R[1, i, 14] = 3
	R[1, i, 15] = 4
	R[1, i, 16] = 5
	R[0, i, 17] = 1
R = R[:, 0:12, : ]

def outputP( year, pitchername ):
	directory = os.fsencode(year + "eve")

	# park - team - date - stats
	statsDict = {}
	playerid = {}
	playerteam = {}

	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		# --------------------- use for search player's team
		if filename.endswith(".ROS"): 
			f = open( "./"+year+"eve/" + filename, "r" )
			data = f.read()
			rows = data.split("\n")
			for row in rows:
				for name in elites:
					if name in row:
						rowarr = row.split(',')
						playerid[name] = rowarr[0]
						playerteam[rowarr[0]] = filename[: -8]
# print(playerteam['hallr001'])

	matchCount = [0]
	prev = 0
	pitcher = playerid[pitchername]
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if playerteam[pitcher] in filename and not filename.endswith('.ROS'):
			teamname = filename[4: 7]
			if teamname not in statsDict:
				statsDict[teamname] = {}
			f = open( "./"+year+"eve/" + filename, "r" )
			data = f.read()
			rows = data.split("\n")
			process.output_home( rows, pitcher, matchCount, statsDict[teamname] )
		# if filename == "2009CHA.EVA":
		elif filename.endswith(".EVN") or filename.endswith(".EVA"): 
			f = open( "./"+year+"eve/" + filename, "r" )
			data = f.read()
			rows = data.split("\n")
			for row in rows:
				if ("start" + pitcher) in row or ("sub" + pitcher) in row:
					teamname = filename[4: 7]
					if filename not in statsDict:
						statsDict[teamname] = {}
					process.output_visit( rows, pitcher, matchCount, statsDict[teamname] ) 
					cur = np.sum(process.p)
					prev = cur
					break;

	sumP = np.sum( process.p, axis=2 ).reshape(2, 18, 1)
	print( np.sum(sumP ))
	index_zero_P = np.argwhere(sumP == 0)
	sumP[sumP==0] = 1
# print(index_zero_P)
	P = np.array( process.p / sumP )
	P = P[:, 0:12, :]
	return P

# print(matchCount[0])
def prettyPrint( unOrderedDict ):
	# count = 0
	anotherDict = {}
	statsDict = collections.OrderedDict(sorted(unOrderedDict.items()))
	for park in statsDict:
		for team in statsDict[park]:
			for date in statsDict[park][team]:
				anotherDict[date] = statsDict[park][team][date]
				# print(" ")
				# print( park, team, date )
				# print( statsDict[park][team][date] )
				# count = count + statsDict[park][team][date]["HR"]
	# print dateordered Dict
	datesDict = collections.OrderedDict(sorted(anotherDict.items()))
	for date in datesDict:
		print( date, "	", datesDict[date])
	# print(count)

# prettyPrint(statsDict)

# process.p[0, 5, 7] = process.p[1, 5, 12] + 7
	# -----------------------------------------------------get P
# sumP = np.sum( process.p, axis=2 ).reshape(2, 18, 1)
# print( np.sum(sumP ))
# index_zero_P = np.argwhere(sumP == 0)
# sumP[sumP==0] = 1
# # print(index_zero_P)
# P = np.array( process.p / sumP )
# P = P[:, 0:12, :]
# for arr in index_zero_P:
#   P[ arr[0], arr[1], arr[1] ] = 1


# if __name__ == "__main__":

# 	c = np.asarray(process.p[1])
# 	np.savetxt("p.csv", c, '%d', delimiter=",")

# 	b = np.asarray(P[0])
# 	np.savetxt("P0.csv", b, '%f', delimiter=",")

# 	a = np.asarray(P[1])
# 	np.savetxt("P1.csv", a, '%f', delimiter=",")

# print(P)
# R = np.zeros((2, 18))
# for aa in range(2):
#   R[aa] = np.sum( np.multiply( P[aa], oR[aa]) , 1 )
# R = R.transpose()
# print(R)
# print(process.p)

# R = np.zeros((18))
# # R[17, 0] = 1
# # R[17, 1] = 1
# R[17] = 1
# # R[13, 0] = 2
# # R[13, 1] = 2
# R[13] = 2
# # R[14, 0] = 3
# # R[14, 1] = 3
# R[14] = 3

# # R[15, 0] = 4
# # R[15, 1] = 4
# R[15] = 4

# # R[16, 0] = 5
# # R[16, 1] = 5
# R[16] = 5

# ----stand and walk
# (3, 0)
# oR[0, 3, 17] = 1
# # (3, 1)
# oR[0, 10, 17] = 1
# # (3, 2)
# oR[0, 11, 17] = 1

# ----swing and single



# header = [
#   "(0, 0)",
#   "(1, 0)",
#   "(2, 0)",
#   "(3, 0)",
#   "(0, 1)",
#   "(0, 2)",
#   "(1, 1)",
#   "(1, 2)",
#   "(2, 1)",
#   "(2, 2)",
#   "(3, 1)",
#   "(3, 2)",
#   "OUT",
#   "S",
#   'D',
#   'T',
#   'HR',
#   'W'
# ]


# tryR = np.zeros(18);
# tryR[17] = 1
# tryR[13] = 2
# tryR[14] = 3
# tryR[15] = 4
# tryR[16] = 5

# print(P)
# print(R)
# mdp.ValueIteration(transitions, reward, discount, epsilon=0.01, max_iter=1000, initial_value=0, skip_check=False)
# vi = mdp.ValueIteration(P, R, 0.9, 2.22 * 10 ** (-16), 100000)

#-------------------------------------------------value iteration
# vi = mdp.value_iteration(P, R, 1, 2.22 * 10 ** (-16), 100, 12, 2)
# policy_V = vi[0]
# print(policy_V)
# J = vi[1]
# print(J)

# J2 = mdp.policy_evaluation(P, R, policy_V, 1, 2.22 * 10 ** (-16), 100, 12, 2)
# print( J2 )

#-------------------------------------------------try
# tryP = [[[1, 0, 1], [1, 0, 1]],[[2, 0, 1], [1, 0, 2]]]
# try1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# try2 = try1
# result = np.multiply( try1, try2 )
# print( np.sum( result, 1 ).shape )

		# print(os.path.join(directory, filename))
