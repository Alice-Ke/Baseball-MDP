import os
import process as pc
import numpy as np
import pandas as pd
import bellman as mdp
import collections

players =[ 
	"Halladay,Roy", #3557 3392 3568 # https://www.baseball-reference.com/players/gl.fcgi?id=hallaro01&t=p&year=2008
	"Lee,Cliff",  #3289 3533 2981 #leecl02
	"Hamels,Cole",#3427 3116 3371  #hamelco01
	"Lester,Jon", #3308 3400 3357 #lestejo01
	"Greinke,Zack", #3231 3477 3345 #greinza01
	"Lincecum,Tim",#3682 3439 3437 #linceti01
	"Sabathia,CC", # 3813 3587 3583 #sabatc.01
	"Santana,Johan", #3598 2575 3004 #santajo02
	"Hernandez,Felix", #3194 3633 3731 #hernafe02
	"Billingsley,Chad", #3322 3250 3134 #billich01
	"Weaver,Jered", #3040 3401 3713 #weaveje02
	"Kershaw,Clayton", #1859 3028 30283390 #kershcl01
	"Carpenter,Chris", #206 2670 3549 #carpech01
	"Garza,Matt", #2947 3420 3281 #garzama01
	"Wainwright,Adam", #1946 3614 3356 #wainwad01
	"Jimenez,Ubaldo", #3350 3570 3600 jimenub01
	"Cain,Matt", #3606 3362 3501 #cainma01
	"Sanchez,Jonathan", #2829 2849 3233 #sanchjo01
	"Oswalt,Roy", #3090 2781 3197#oswalro01
	"Verlander,Justin", #3528 3937 3745 #verlaju01
	"Johnson,Josh", #1411 3284 2988 #johnsjo09
	"Danks,John", #3144 3210 3389 #danksjo01
	"Jackson,Edwin", #3056 3466 3358 #jacksed01
	"Scherzer,Max", #929 3073 3301 #scherma01
	"Lilly,Ted", #3240 2671 2907 #lillyte01

	# 25

	"Lowe,Derek",
	"Penny,Brad",
	"Hammel,Jason",
	"Masterson,Justin",
	"Porcello,Rick",
	# "Romero,Ricky",
	"Saunders,Joe",
	"Hamels,Cole",
	"Hernandez,Livan",
	# "Looper,Braden",
	"Jackson,Edwin",
	# "Hellickson,Jeremy",
	# "Moyer,Jamie",
	"Pelfrey,Mike",
	"Blanton,Joe",
	"Millwood,Kevin",
	"Guthrie,Jeremy",
	"Cahill,Trevor",
	# "Dempster,Jerome",
	# "Pavano,Carl", //1
	"Cueto,Johnny",
	"Francis,Jeff",
	# "Bush,David", //1
	"Baker,Scott",
	# "Niemann,Jeff", //1
	"Volstad,Chris",
	"Kendrick,Kyle",
	"Maholm,Paul",
	"Myers,Brett",
	# "Lewis,Colby",
	"Morton,Charlie",
	# "Olsen,Scott",
	"Weaver,Jered",
	# "Duke,Zach", //1
	# "Redding,Tim",
	# "Snell,Ian",
	"Bannister,Brian"

	# 24
]



def ifContains(l, filename):
	for e in l:
		if e in filename:
			return True
	return False


class Stat():

	def __init__(self):
		self.process = pc.Process()

	def outputP( self, year, pitchername, playerteam, playerid ):
		directory = os.fsencode(year + "eve")

		# park - team - date - stats
		statsDict = {}

		# playerid = {}
		# playerteam = {}

		# for file in os.listdir(directory):
		# 	filename = os.fsdecode(file)
		# 	# --------------------- use for search player's team
		# 	if filename.endswith(".ROS"): 
		# 		f = open( "./"+year+"eve/" + filename, "r" )
		# 		data = f.read()
		# 		rows = data.split("\n")
		# 		for row in rows:
		# 			for name in players:
		# 				if name in row:
		# 					rowarr = row.split(',')
		# 					playerid[name] = rowarr[0]
		# 					if rowarr[0] not in playerteam:
		# 						playerteam[rowarr[0]] = []
		# 					playerteam[rowarr[0]].append(filename[: -8])

		# print(playerteam)

		matchCount = [0]
		prev = 0
		# if the pitcher is not in this year
		if pitchername not in playerid:
			return None
		pitcher = playerid[pitchername]
		for file in os.listdir(directory):
			filename = os.fsdecode(file)
			# for diffteam in playerteam[pitcher]:
			if ifContains(playerteam[pitcher], filename) and not filename.endswith('.ROS'):
				# print(filename)
				teamname = filename[4: 7]
				if teamname not in statsDict:
					statsDict[teamname] = {}
				f = open( "./"+year+"eve/" + filename, "r" )
				data = f.read()
				rows = data.split("\n")
				self.process.output_home( rows, pitcher, matchCount, statsDict[teamname] )
			# if filename == "2009CHA.EVA":
			elif filename.endswith(".EVN") or filename.endswith(".EVA"): 
				f = open( "./"+year+"eve/" + filename, "r" )
				data = f.read()
				rows = data.split("\n")
				for row in rows:
					if ("start," + pitcher) in row or ("sub," + pitcher) in row:
						# print(filename)
						teamname = filename[4: 7]
						if filename not in statsDict:
							statsDict[teamname] = {}
						self.process.output_visit( rows, pitcher, matchCount, statsDict[teamname] ) 
						cur = np.sum(self.process.p)
						prev = cur
						break;

		sumP = np.sum( self.process.p, axis=2 ).reshape(2, 18, 1)
		sumP[sumP==0] = 1
	# print(index_zero_P)
		P = np.array( self.process.p / sumP )
		P = P[:, 0:12, :]
		return (self.process.p, P, statsDict)

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


if __name__ == "__main__":

	# stat = Stat()
	# a, b, c = stat.outputP("2009","Lee,Cliff" )
	# print(c)
	print(len( elites) )

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
