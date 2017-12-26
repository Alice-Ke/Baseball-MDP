# author: Pu Ke, 
# uni: pk2532

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
	"Duke,Zach", 
	# "Redding,Tim",
	# "Snell,Ian",
	"Bannister,Brian"
	# 25

	#2000
	"Martinez,Pedro",
	"Brown,Kevin",
	"Johnson,Randy",
	"Maddux,Greg",
	"Hampton,Mike",
	#2001
	"Schilling,Curt",
	"Burkett,John",
	"Garcia,Freddy",
	"Mays,Joe",
	"Buehrle,Mark",
	#2002
	"Zito,Barry",
	"Hudson,Tim",
	"Oswalt,Roy",
	"Wolf,Randy",

	#14

	#80s
	# "Key,Jimmy",
	# "Higuera,Teddy",
	# "Hough,Charlie",
	# "Stewart,Dave",
	# "Sutcliffe,Rick",
	# "Tudor,John",
	# "Viola,Frank",
	# "Carlton,Steve",
	# "Guidry,Ron",
	# "Scott,Mike",
	# "Blyleven,Bert",
	# "Welch,Bob",
	# "Valenzuela,Fernando",
	# "Stieb,Dave",
	# "Ryan,Nolan",
	# "Saberhagen,Bret",
	# "Hershiser,Orel",
	# "Morris,Jack",
	# "Clemens,Roger",
	# "Gooden,Dwight",

	#90s
	"Nomo,Hideo",
	"Stottlemyre,Todd",
	"Leiter,Ai",
	"Tapani,Kevin",
	"Rogers,Kenny",
	"Guzman,Juan",
	"Fernandez,Alex",
	"Hentgen,Pat",
	"Benes,Andy",
	"Erickson,Scott",
	"Nagy,Charles",
	"Martinez,Dennis",
	"Martinez,Ramon",
	"Pettitte,Andy",
	"Wells,David",
	"Mcdowell,Jack",
	"Rijo,Jose",
	"Finley,Chuck",
	"Appier,Kevin",
	"Smoltz,John",
	"Cone,David",
	"Mussina,Mike",
	"Glavine,Tom"
    #23


]

# players =[ 
# 	"Halladay,Roy", #3557 3392 3568 # https://www.baseball-reference.com/players/gl.fcgi?id=hallaro01&t=p&year=2008
# 	"Lee,Cliff",  #3289 3533 2981 #leecl02
# 	"Hamels,Cole",#3427 3116 3371  #hamelco01
# 	"Lester,Jon", #3308 3400 3357 #lestejo01
# 	"Greinke,Zack", #3231 3477 3345 #greinza01
# 	"Lincecum,Tim",#3682 3439 3437 #linceti01
# 	"Sabathia,CC", # 3813 3587 3583 #sabatc.01
# 	"Santana,Johan", #3598 2575 3004 #santajo02
# 	"Hernandez,Felix", #3194 3633 3731 #hernafe02
# 	"Billingsley,Chad", #3322 3250 3134 #billich01
# 	"Weaver,Jered", #3040 3401 3713 #weaveje02
# 	"Kershaw,Clayton", #1859 3028 30283390 #kershcl01
# 	"Carpenter,Chris", #206 2670 3549 #carpech01
# 	"Garza,Matt", #2947 3420 3281 #garzama01
# 	"Wainwright,Adam", #1946 3614 3356 #wainwad01
# 	"Jimenez,Ubaldo", #3350 3570 3600 jimenub01
# 	"Cain,Matt", #3606 3362 3501 #cainma01
# 	"Sanchez,Jonathan", #2829 2849 3233 #sanchjo01
# 	"Oswalt,Roy", #3090 2781 3197#oswalro01
# 	"Verlander,Justin", #3528 3937 3745 #verlaju01
# 	"Johnson,Josh", #1411 3284 2988 #johnsjo09
# 	"Danks,John", #3144 3210 3389 #danksjo01
# 	"Jackson,Edwin", #3056 3466 3358 #jacksed01
# 	"Scherzer,Max", #929 3073 3301 #scherma01
# 	"Lilly,Ted", #3240 2671 2907 #lillyte01

# 	# 25

# 	"Lowe,Derek",
# 	"Penny,Brad",
# 	"Hammel,Jason",
# 	"Masterson,Justin",
# 	"Porcello,Rick",
# 	# "Romero,Ricky",
# 	"Saunders,Joe",
# 	"Hamels,Cole",
# 	"Hernandez,Livan",
# 	# "Looper,Braden",
# 	"Jackson,Edwin",
# 	# "Hellickson,Jeremy",
# 	# "Moyer,Jamie",
# 	"Pelfrey,Mike",
# 	"Blanton,Joe",
# 	"Millwood,Kevin",
# 	"Guthrie,Jeremy",
# 	"Cahill,Trevor",
# 	# "Dempster,Jerome",
# 	# "Pavano,Carl", //1
# 	"Cueto,Johnny",
# 	"Francis,Jeff",
# 	# "Bush,David", //1
# 	"Baker,Scott",
# 	# "Niemann,Jeff", //1
# 	"Volstad,Chris",
# 	"Kendrick,Kyle",
# 	"Maholm,Paul",
# 	"Myers,Brett",
# 	# "Lewis,Colby",
# 	"Morton,Charlie",
# 	# "Olsen,Scott",
# 	"Weaver,Jered",
# 	"Duke,Zach", 
# 	# "Redding,Tim",
# 	# "Snell,Ian",
# 	"Bannister,Brian"

# 	# 25
# ]



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
						teamname = filename[4: 7]
						if filename not in statsDict:
							statsDict[teamname] = {}
						self.process.output_visit( rows, pitcher, matchCount, statsDict[teamname] ) 
						cur = np.sum(self.process.p)
						prev = cur
						break;

		sumP = np.sum( self.process.p, axis=2 ).reshape(2, 18, 1)
		sumP[sumP==0] = 1
		P = np.array( self.process.p / sumP )
		P = P[:, 0:12, :]
		return (self.process.p, P, statsDict)

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


# if __name__ == "__main__":

	# print(len( elites) )


