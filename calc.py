# author: Pu Ke, 
# uni: pk2532

import os
import process
import stats
import numpy as np
import pandas as pd
import bellman as mdp
import collections
import csv
import pickle



# pitcherProb = {}
# generalProb = {}
# =====================================================================
pitcherProb = pickle.load( open( "pitcherProb.p", "rb" ) )
generalProb = pickle.load( open( "generalProb.p", "rb" ) )
# =====================================================================
pitcherPolicy = {}
generalPolicy = {}

pitcherV = {}
generalV = {}

intuitivePolicy = [ 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0 ]

totalYears = []
for i in range( 1991, 2018 ):
	totalYears.append( str(i) )

trainlabels = ["g", "p", "i"]

def produceStats( year, name, playerteam, playerid ):
	stat = stats.Stat()
	return stat.outputP( year , name, playerteam, playerid ) 

# return big p sum, dict: name - P, statsDict
def prooduceGeneralStats( year ):
	print(" ")
	print( "iterate through players in year: ", year, ", to gather the probability" )
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
		bigpsum = np.add(bigpsum, np.divide( sump[:, 0:12, :], 50 ) )
		# bigpsum = np.add( bigpsum, sump[:, 0:12, :])
		# stats.prettyPrint(statsDict)
		print("total pitch counts: ", np.sum( np.sum( sump ) ) )
	
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

def calculateDiffPlayers( S, D, T, HR, W ):
	# =====================================================================
	# for year in totalYears:
	# 	prooduceGeneralStats(year)
	# pickle.dump(generalProb , open( "generalProb.p", "wb" ) )
	# pickle.dump(pitcherProb, open( "pitcherProb.p", "wb" ) )
	# =====================================================================
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

	for key in pitcherProb:
		vi = mdp.value_iteration(pitcherProb[key], R, 1, 2.22 * 10 ** (-16), 100, 12, 2)
		pitcherPolicy[key] = vi[0]

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
		name = stats.players[i]
		for trainYear in totalYears:
			for testYear in totalYears:
				if trainYear != testYear:
					keyprefix = name + trainYear + testYear
					for trainlabel in trainlabels:
						evaluateResult = evaluate( R, name, trainlabel, trainYear, testYear )[0]
						resultDict[keyprefix + trainlabel] = evaluateResult
					if( resultDict[keyprefix + 'i'] == None or resultDict[keyprefix + 'g'] == None or resultDict[keyprefix + 'p'] == None ):
						continue
					if i <= 24:
						totalCountElites = totalCountElites + 1
					else:
						totalCountNonElites = totalCountNonElites + 1

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

	# print( intuitiveCountElites,pitcherCountElites,generalCountElites )
	# print(" ")
	# print( intuitiveCountNonElites,pitcherCountNonElites,generalCountNonElites)
	# print( resultDict )

	for key in resultDict:
		if resultDict[key] != None:
			print( "the evaluation result for ‘name-trainYear-testYear-label ", key, ", is: ", resultDict[key] )
	return ( resultCountElites/totalCountElites, resultCountNonElites/totalCountNonElites, (resultCountElites+resultCountNonElites)/(totalCountElites+totalCountNonElites) )

def reverseRL():
	# =====================================================================
	# for year in totalYears:
	# 	prooduceGeneralStats(year)
	# pickle.dump(generalProb , open( "generalProb.p", "wb" ) )
	# pickle.dump(pitcherProb, open( "pitcherProb.p", "wb" ) )
	# =====================================================================
	print("reverse reinforcement learning to calculate best rewards for S, D, T, HR, W" )
	W = 1
	S = 1
	maxElite = 0
	maxNonElite = 0
	maxTotal = 0
	maxElitePara = (0,0,0,0,0)
	maxNonElitePara = (0,0,0,0,0)
	maxTotalPara = (0,0,0,0,0)
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
					print("S, D, T, HR, W: ", S, D, T, HR, W )
					resElite, resNonElite, resTotal = calculateDiffPlayers(S, D, T, HR, W) 
					if resElite >= maxElite:
						maxElite = resElite
						maxElitePara = ( S, D, T, HR, W )
					if resNonElite >= maxNonElite:
						maxNonElite = resNonElite
						maxNonElitePara = ( S, D, T, HR, W )
					if resTotal >= maxTotal:
						maxTotal = resTotal
						maxTotalPara = ( S, D, T, HR, W )

					print("policy evaluation for elites, non-elites and totoal: ", calculateDiffPlayers(S, D, T, HR, W) )
	print( maxElite, maxElitePara )
	print( maxNonElite, maxNonElitePara )
	print( maxTotal, maxTotalPara )

def getDiffYearPolicy():
	# =====================================================================
	# for year in totalYears:
	# 	prooduceGeneralStats(year)
	# pickle.dump(generalProb , open( "generalProb.p", "wb" ) )
	# pickle.dump(pitcherProb, open( "pitcherProb.p", "wb" ) )
	# =====================================================================
	R = np.zeros((2, 12, 18))
	for i in range(12):
		R[1, i, 13] = 2 #1.5 
		R[1, i, 14] = 3 #2.0 
		R[1, i, 15] = 4 #2.5 
		R[1, i, 16] = 5 #3.0 
		R[0, i, 17] = 1.0

	for key in generalProb:
		vi = mdp.value_iteration(generalProb[key], R, 1, 2.22 * 10 ** (-16), 100, 12, 2)
		generalPolicy[key] = vi[0]


	for key in pitcherProb:
		vi = mdp.value_iteration(pitcherProb[key], R, 1, 2.22 * 10 ** (-16), 100, 12, 2)
		pitcherPolicy[key] = vi[0]

		
	for key in sorted(generalPolicy):
		print( "calculate genral policy for year: ", key, ", the policy is: ", generalPolicy[key] )

	for key in sorted(pitcherPolicy):
		print( "calculate pitcher-specific policy for year+pitcher: ", key, ", the policy is: ", pitcherPolicy[key] )

		

if __name__ == '__main__':

	# get the general policies for 27 years:
	getDiffYearPolicy()

	# get the evaluation results for each train/test pair: 
	# calculateDiffPlayers( 2, 3, 4, 5, 1 )

	# reward function tuning part:
	# reverseRL()
	