import os
import process
import stats
import numpy as np
import pandas as pd
import bellman as mdp
import collections
import csv
import pickle

# input: year, name
# return: sump, P, statsdict

pitcherProb = {}
generalProb = {}
# =====================================================================
# pitcherProb = pickle.load( open( "pitcherProb.p", "rb" ) )
# generalProb = pickle.load( open( "generalProb.p", "rb" ) )
# =====================================================================
pitcherPolicy = {}
generalPolicy = {}

pitcherV = {}
generalV = {}

intuitivePolicy = [ 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0 ]

years = ["2008", "2009", "2010", "2011", "2012", "2013"]
trainlabels = ["g", "p", "i"]

def produceStats( year, name, playerteam, playerid ):
	stat = stats.Stat()
	return stat.outputP( year , name, playerteam, playerid ) 

# return big p sum, dict: name - P, statsDict
def prooduceGeneralStats( year ):
	directory = os.fsencode(year + "eve")

		# park - team - date - stats
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
				for name in stats.players:
					if name in row:
						rowarr = row.split(',')
						playerid[name] = rowarr[0]
						if rowarr[0] not in playerteam:
							playerteam[rowarr[0]] = []
						playerteam[rowarr[0]].append(filename[: -8])

	bigpsum = np.zeros((2, 12, 18))
	for e in stats.players:
		print(" ")
		print(year, e)
		if( produceStats( year, e, playerteam, playerid) == None ):
			print( None )
			continue
		sump, P, statsDict = produceStats( year, e, playerteam, playerid  )
		pitcherProb[year+e] = P
		# bigpsum = np.add(bigpsum, np.divide( sump[:, 0:12, :], 25 ) )
		bigpsum = np.add( bigpsum, sump[:, 0:12, :])
		# stats.prettyPrint(statsDict)
		print(np.sum( np.sum( sump ) ) )
	
	sumP = np.sum( bigpsum, axis=2 ).reshape(2, 12, 1)
	sumP[sumP==0] = 1
	P = np.array( bigpsum / sumP )
	generalProb[year] = P

	# c = np.asarray(P[1])
	# np.savetxt("sumP.csv", c, '%f', delimiter=",")
	# print(bigpsum)
	# print(count)
	# print(np.sum( np.sum( bigpsum ) ) )

def evaluate( R, pitcher, trainLabel, trainYear, testYear ):
	if trainLabel == "g":
		testKey = testYear+pitcher
		if testKey not in pitcherProb:
			return [None]
		prob = pitcherProb[testKey]
		policy = generalPolicy[trainYear]
		V = mdp.policy_evaluation(prob, R, policy, 1, 2.22 * 10 ** (-16), 100, 12, 2)
		return V 
	if trainLabel == "p":
		testKey = testYear + pitcher
		trainKey = trainYear + pitcher
		if testKey not in pitcherProb or trainKey not in pitcherProb:
			return [None]
		prob = pitcherProb[testKey]
		policy = pitcherPolicy[trainKey]
		V = mdp.policy_evaluation(prob, R, policy, 1, 2.22 * 10 ** (-16), 100, 12, 2)
		return V 
	if trainLabel == "i":
		testKey = testYear+pitcher
		if testKey not in pitcherProb:
			return [None]
		prob = pitcherProb[testKey]
		policy = intuitivePolicy
		V = mdp.policy_evaluation(prob, R, policy, 1, 2.22 * 10 ** (-16), 100, 12, 2)
		return V

# print( J2010 )

# writer.writerow(["name", "Train2008_Test2009_g", "Train2008_Test2009_p","Train2008_Test2009_i", "Train2008_Test2010_g","Train2008_Test2010_p", "Train2008_Test2010_i", 
# 						"Train2009_Test2008_g","Train2009_Test2008_p", "Train2009_Test2008_i", "Train2009_Test2010_g", "Train2009_Test2010_p", "Train2009_Test2010_i", 
# 						"Train2010_Test2008_g", "Train2010_Test2008_p","Train2010_Test2008_i", "Train2010_Test2009_g", "Train2010_Test2009_p", "Train2010_Test2009_i" ])
 


# compareDict = {
# 	"20082009": 0,
# 	"20082010": 0,
# 	"20092008": 0,
# 	"20092010": 0,
# 	"20102008": 0,
# 	"20102009": 0
# }
def calculateDiffPlayers( S, D, T, HR, W ):
	R = np.zeros((2, 12, 18))
	for i in range(12):
		R[1, i, 13] = S
		R[1, i, 14] = D
		R[1, i, 15] = T
		R[1, i, 16] = HR
		R[0, i, 17] = W

	for key in generalProb:
		vi = mdp.value_iteration(generalProb[key], R, 1, 2.22 * 10 ** (-16), 100, 12, 2)
		generalPolicy[key] = vi[0]
		# print( key )
		# print( vi[0] )

	for key in pitcherProb:
		vi = mdp.value_iteration(pitcherProb[key], R, 1, 2.22 * 10 ** (-16), 100, 12, 2)
		pitcherPolicy[key] = vi[0]
		# print( key )
		# print( vi[0] )
# csv part
	# outcsv=open('./result.csv','w')
	# writer = csv.writer(outcsv)
	# headerrow = ["name"]
	# for trainYear in years:
	# 	for testYear in years:
	# 		if trainYear != testYear:
	# 			for trainlabel in trainlabels:
	# 				header = trainYear + testYear + trainlabel
	# 				headerrow.append( header )
	# writer.writerow(headerrow)

	resultDict = {}
	totalCountElites = 0
	intuitiveCountElites = 0
	generalCountElites = 0
	pitcherCountElites = 0
	totalCountNonElites = 0
	intuitiveCountNonElites = 0
	generalCountNonElites = 0
	pitcherCountNonElites = 0

	resultCountElites = 0
	resultCountNonElites = 0
	
	for i in range( len( stats.players ) ):
		csvrow = []
		name = stats.players[i]
		csvrow.append( name )
		for trainYear in years:
			for testYear in years:
				if trainYear != testYear:
					keyprefix = name + trainYear + testYear
					for trainlabel in trainlabels:
						evaluateResult = evaluate( R, name, trainlabel, trainYear, testYear )[0]
						csvrow.append( evaluateResult )
						resultDict[keyprefix + trainlabel] = evaluateResult
					# if( resultDict[keyprefix + 'p'] > resultDict[keyprefix + 'g'] ):
					# 	compareDict[trainYear+testYear] = compareDict[trainYear+testYear] + 1
					if( resultDict[keyprefix + 'i'] == None or resultDict[keyprefix + 'g'] == None or resultDict[keyprefix + 'p'] == None ):
						continue
					if i <= 24:
						totalCountElites = totalCountElites + 1
					else:
						totalCountNonElites = totalCountNonElites + 1
# csv part
					# if( resultDict[keyprefix + 'i'] > resultDict[keyprefix + 'g'] and resultDict[keyprefix + 'i'] > resultDict[keyprefix + 'p'] ):
					# 	if i <= 24:
					# 		intuitiveCountElites = intuitiveCountElites + 1
					# 	else:
					# 		intuitiveCountNonElites = intuitiveCountNonElites + 1
					# if( resultDict[keyprefix + 'p'] > resultDict[keyprefix + 'i'] and resultDict[keyprefix + 'p'] > resultDict[keyprefix + 'g'] ):
					# 	if i <= 24:
					# 		pitcherCountElites = pitcherCountElites + 1
					# 	else:
					# 		pitcherCountNonElites = pitcherCountNonElites + 1
					# if( resultDict[keyprefix + 'g'] > resultDict[keyprefix + 'i'] and resultDict[keyprefix + 'g'] > resultDict[keyprefix + 'p'] ):
					# 	if i <= 24:
					# 		generalCountElites = generalCountElites + 1
					# 	else:
					# 		generalCountNonElites = generalCountNonElites + 1

					if( resultDict[keyprefix + 'g'] > resultDict[keyprefix + 'i'] ):
						if i <= 24:
							resultCountElites = resultCountElites + 1
						else:
							resultCountNonElites = resultCountNonElites + 1
	return ( resultCountElites/totalCountElites, resultCountNonElites/totalCountNonElites )

# csv part
		# writer.writerow( csvrow )

		# compare elites and nonelites general stats
	# print(" Elites ")
	# print( intuitiveCountElites / totalCountElites )
	# print( pitcherCountElites / totalCountElites )
	# print( generalCountElites / totalCountElites )

	# print(" NonElites ")
	# print( intuitiveCountNonElites / totalCountNonElites )
	# print( pitcherCountNonElites / totalCountNonElites )
	# print( generalCountNonElites / totalCountNonElites )

if __name__ == '__main__':

	# =====================================================================
	for year in years:
		prooduceGeneralStats(year)
	pickle.dump(generalProb , open( "generalProb.p", "wb" ) )
	pickle.dump(pitcherProb, open( "pitcherProb.p", "wb" ) )
	# =====================================================================

	W = 1
	S = 1
	maxElite = 0
	maxNonElite = 0
	maxElitePara = (0,0,0,0,0)
	maxNonElitePara = (0,0,0,0,0)
	step = 0.5
	while S < 3:
		S = S + step
		D = S
		while D < 4.5:
			D = D + step
			T = D
			while T < 6:
				T = T + step
				HR = T
				while HR < 7.5:
					HR = HR + step
					print(" ")
					print( S, D, T, HR, W )
					resElite, resNonElite = calculateDiffPlayers(S, D, T, HR, W) 
					if resElite >= maxElite:
						maxElite = resElite
						maxElitePara = ( S, D, T, HR, W )
					if resNonElite >= maxNonElite:
						maxNonElite = resNonElite
						maxNonElitePara = ( S, D, T, HR, W )

					print( calculateDiffPlayers(S, D, T, HR, W) )
	print( maxElite, maxElitePara )
	print( maxNonElite, maxNonElitePara )
	
   
# print(" ")
# stat1 = stats.Stat()
# e, P2009Hallady, statsDict2009Hallady = stat1.outputP("2009", "Halladay,Roy" ) 
# stats.prettyPrint( statsDict2009Hallady )
# # print(P2009Hallady)

# print(" ")
# stat2 = stats.Stat()
# e, P2010Hallady, statsDict2010Hallady = stat2.outputP("2010", "Halladay,Roy" ) 
# stats.prettyPrint( statsDict2010Hallady )
# print(P2010Hallady)

# # ---------------------------------------------
# print(" ")
# vi = mdp.value_iteration(P2009Hallady, stats.R, 1, 2.22 * 10 ** (-16), 100, 12, 2)
# policy_V2009Hallady = vi[0]
# print(policy_V2009Hallady)

# J2010 = mdp.policy_evaluation(P2010Hallady, stats.R, policy_V2009Hallady, 1, 2.22 * 10 ** (-16), 100, 12, 2)
# print( J2010 )
# vi = mdp.value_iteration(P2010Hallady, stats.R, 1, 2.22 * 10 ** (-16), 100, 12, 2)
# policy_V2010Hallady = vi[0]
# print(policy_V2010Hallady)

# J2008 = mdp.policy_evaluation(P2008Hallady, stats.R, policy_V2009Hallady, 1, 2.22 * 10 ** (-16), 100, 12, 2)
# print( J2008 )
# vi = mdp.value_iteration(P2008Hallady, stats.R, 1, 2.22 * 10 ** (-16), 100, 12, 2)
# policy_V2008Hallady = vi[0]
# print(policy_V2008Hallady)