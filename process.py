# author: Pu Ke, 
# uni: pk2532
import re
import numpy as np


states = {
	(0, 0): 0,
	(1, 0): 1,
	(2, 0): 2,
	(3, 0): 3, #before walk: 0
	(0, 1): 4,
	(0, 2): 5,
	(1, 1): 6,
	(1, 2): 7,
	(2, 1): 8,
	(2, 2): 9,
	(3, 1): 10, #before walk: 0
	(3, 2): 11, #before walk: 0

	# strike out
	(0, 3): 12,
	(1, 3): 12,
	(2, 3): 12,
	(3, 3): 12,   
	#
	'OUT': 12,
	'S': 13, 
	'D': 14,
	'T': 15,
	'HR': 16,
	# walk
	'W': 17,
	(4, 0): 17,
	(4, 1): 17,
	(4, 2): 17

}
# out: 12
# single: 13
# double: 14
# triple: 15
# homerun: 16
# walk: 17
def returnDict():
	return{
		"Pitches": 0,
		"FC": 0,
		"H": 0,
		"HR": 0,
		"BB": 0,
		"2B": 0,
		"3B": 0
	}

class Process():
	def __init__(self):	
		self.p = np.zeros( (2, 18, 18) )

	def countstate( self, line, dateDict ):
		arr = line.split(',')
		info = arr[5]
		
		res = arr[6]
		# ball, strike
		start = (0,0)
		prev = (0,0)
		# print( info, res )
		for i in range( len( info ) ):
			cur_info = info[i]
			# ball or pitch out
			if( cur_info in [ 'B', 'P', 'I' ] ):
				dateDict["Pitches"] = dateDict["Pitches"] + 1
				cur = (prev[0] + 1, prev[1])
				action = 0
				if cur[0] == 4:
					dateDict["BB"] = dateDict["BB"] + 1
			# called strike
			elif( cur_info  == 'C' ):
				dateDict["Pitches"] = dateDict["Pitches"] + 1
				cur = (prev[0], prev[1] + 1)
				action = 0
			# Swing and strike
			elif( cur_info in['S', 'L', 'T', 'K', 'M' ] ):
				dateDict["Pitches"] = dateDict["Pitches"] + 1
				# print(line)
				cur = (prev[0], prev[1] + 1 )
				action = 1
			# Foul ball when counts == 2
			elif( cur_info == 'F' and prev[1] == 2 ):
				dateDict["Pitches"] = dateDict["Pitches"] + 1
				# print( line )
				cur = prev
				action = 1
			# Foul ball when counts < 2
			elif( cur_info == 'F' and prev[1] < 2 ):
				dateDict["Pitches"] = dateDict["Pitches"] + 1
				# print( line, prev )
				cur = (prev[0], prev[1] + 1)
				action = 1
			# hit by the pitcher
			elif( cur_info == 'H'):
				dateDict["Pitches"] = dateDict["Pitches"] + 1
				# print( line, prev )
				cur = 'W'
				action = 0
			# hit out
			elif( cur_info == 'X'):
				dateDict["Pitches"] = dateDict["Pitches"] + 1
				# print(res)
				action = 1
				first = res[0]
				dateDict["H"] = dateDict["H"] + 1
				if( re.match(r'\d', first)):
					# print(first)
					cur = 'OUT'
				elif( first == 'E' ):
					# print(line)
					cur = 'OUT'
				elif( first == 'S' ):
					cur = 'S'
				elif( first == 'D' ):
					cur = 'D'
					dateDict["2B"] = dateDict["2B"] + 1
				elif( first == 'T' ):
					cur = 'T'
					dateDict["3B"] = dateDict["3B"] + 1
				elif( res[0:2] == 'HR' ):
					cur = 'HR'
					dateDict["HR"] = dateDict["HR"] + 1
				elif( res[0:2] == 'FC' ):
					cur = 'OUT'
					dateDict["FC"] = dateDict["FC"] + 1
				# eg. catcher inference
				else:
					# print(line)
					continue
			else:
				# print(line, cur_info)
				continue
			# add trans to matrix
			self.p[action, states[prev], states[cur]] = self.p[action, states[prev], states[cur]] + 1
			prev = cur


	def output_home( self, lines, name, matchCount, teamsDict ):
		i = 0
		count = 0
		while i < len( lines ):
			if ( "start," + name ) in lines[i]:
				j = i 
				while j >= 0:
					if re.match(r'info,date,.*', lines[j] ):
						date = lines[j][10: ]
						matchCount[0] = matchCount[0] + 1
						team = lines[j-3][13: ]
						if team not in teamsDict:
							teamsDict[team] = {}
						if date not in teamsDict[team]:
							teamsDict[team][date] = returnDict()
						break;
					j = j - 1
				# find the next sub in home data
				i = i + 1
				while i < len(lines) and re.match(r'sub,.*,.*,1,\d,1$', lines[i]) is None and re.match(r'id,.*', lines[i]) is None:
					m = re.match(r'play,\d,0', lines[i])
					if m is not None:
						if i >= len(lines) - 1 or re.match(r'play,\d,0', lines[i+1]) is None :
							flag = True
						else:
							player = lines[i].split(',')[3]
							postPlayer = lines[i+1].split(',')[3]
							flag = player != postPlayer
						if flag:
							self.countstate( lines[i], teamsDict[team][date] )
					i = i + 1
			elif ( "sub," + name ) in lines[i]:
				j = i 
				while j >= 0:
					if re.match(r'info,date,.*', lines[j] ):
						date = lines[j][10: ]
						matchCount[0] = matchCount[0] + 1
						team = lines[j-3][13: ]
						if team not in teamsDict:
							teamsDict[team] = {}
						if date not in teamsDict[team]:
							teamsDict[team][date] = returnDict()
						break;
					j = j - 1
				i = i + 1
				while i < len(lines) and re.match(r'sub,.*,.*,1,\d,1$', lines[i]) is None and re.match(r'id,.*', lines[i]) is None:
					m = re.match(r'play,\d,0', lines[i])
					if m is not None:
						if i == len(lines) - 1 or re.match(r'play,\d,0', lines[i+1]) is None :
							flag = True
						else:
							player = lines[i].split(',')[3]
							postPlayer = lines[i+1].split(',')[3]
							flag = player != postPlayer
						if flag:

							# print(lines[i])

							self.countstate( lines[i], teamsDict[team][date] )
					i = i + 1           
			i = i + 1

	def output_visit( self, lines, name, matchCount, teamsDict ):
		i = 0
		while i < len( lines ):
			if ( "start," + name ) in lines[i]:
				# find the date of the match
				j = i 
				while j >= 0:
					if re.match(r'info,date,.*', lines[j] ):
						date = lines[j][10: ]
						matchCount[0] = matchCount[0] + 1
						team = lines[j-2][14: ]
						if team not in teamsDict:
							teamsDict[team] = {}
						if date not in teamsDict[team]:
							teamsDict[team][date] = returnDict()
						break;
					j = j - 1
				# find the next sub in home data
				i = i + 1
				while i < len(lines) and re.match(r'sub,.*,.*,0,\d,1$', lines[i]) is None and re.match(r'id,.*', lines[i]) is None:
					m = re.match(r'play,\d,1', lines[i])
					if m is not None:
						
						if i == len(lines) - 1 or re.match(r'play,\d,1', lines[i+1]) is None :
							flag = True
						else:
							player = lines[i].split(',')[3]
							postPlayer = lines[i+1].split(',')[3]
							flag = player != postPlayer
						if flag:
							self.countstate( lines[i], teamsDict[team][date] )

					i = i + 1
			elif ( "sub," + name ) in lines[i]:
				j = i 
				while j >= 0:
					if re.match(r'info,date,.*', lines[j] ):
						date = lines[j][10: ]
						matchCount[0] = matchCount[0] + 1
						team = lines[j-3][13: ]
						if team not in teamsDict:
							teamsDict[team] = {}
						if date not in teamsDict[team]:
							teamsDict[team][date] = returnDict()
						break;
					j = j - 1
				i = i + 1
				while i < len(lines) and re.match(r'sub,.*,.*,0,\d,1$', lines[i]) is None and re.match(r'id,.*', lines[i]) is None:
					m = re.match(r'play,\d,1', lines[i])
					if m is not None:
						if i == len(lines) - 1 or re.match(r'play,\d,1', lines[i+1]) is None :
							flag = True
						else:
							
							player = lines[i].split(',')[3]
							postPlayer = lines[i+1].split(',')[3]
							flag = player != postPlayer
						if flag:
							self.countstate( lines[i], teamsDict[team][date] )
					i = i + 1           
			i = i + 1

# ------------------------------------------------------module test
if __name__ == "__main__":

	p = Process()
	f = open( "./2009eve/" + "2009CLE.EVA", "r" )
	data = f.read()
	rows = data.split("\n")
	m = [0]
	t = {}
	p.output_home(rows, "lee-c003", m, t )
	print(t)
	# A = np.asarray(process.p[0])
	# header = process.states.keys()
	# df = pd.DataFrame(A, index=header, columns=header)
	# df.to_csv('df.csv', index=True, header=True, sep=' ')
	# print(p)

	# ------------------------------------------------------state test
	# countstate("play,9,0,grifk002,21,BFBX,3/P3F")
	# countstate("play,1,0,granc001,31,BCBBB,W")
	# countstate("play,8,0,saunm001,22,CBBFFFS,K")
	# countstate("play,5,0,buscb001,10,BX,S9/L")
	# countstate("play,6,0,teixm001,32,BBBFF*B,W.2-3;1-2")
	# countstate("play,6,0,hinse001,32,SBBFBB,W")
	# countstate("play,5,0,bay-j001,00,X,HR/7/F.2-H(UR)")
	# countstate("play,4,0,moram002,22,CFBBFFFFFX,4/P")
	# countstate("play,8,0,crawc002,02,TFS,K")
	# countstate("play,5,0,hernm002,01,FX,9/F")

	# ------------------------------------------------------reg expression test
	# m1 = re.match(r'play,\d,0', "play,7,0,evera001,21,BFBX,9/F")
	# m = re.match(r'sub,.*,.*,1', "sub,carlj001,Jesse Carlson,1,0,1") 
	# print(m1)
	# print(m)