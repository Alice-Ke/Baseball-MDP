# # import re
# # import numpy as np
# # # a = {
	
# # # 	"Alice" :{
# # # 		"age": 1
# # # 	}
# # # }

# # # a["Alice"]["sex"] = "lady"
# # # a["Joy"] = {}
# # # a["Joy"]["age"] = 2

# # # dateDict = {
# # # 	"HR" : 0
# # # }
# # # dateDict["HR"] = dateDict["HR"] + 1
# # # print(dateDict)

# # # line = "sub,bautj002,Jose Bautista,0,9,1"
# # # print( re.match(r'sub,.*,.*,0,\d,1$', line ) )


# # # for i in range(4):
# # # 	# if i == 1:
# # # 	# 	print(i)
# # # 	# else:
# # # 		# continue
# # # 	print(i)

# # P = np.array([
# # [
# # 	[0, 3/4, 1/4, 0],
# # 	[0, 1, 0, 0],
# # 	[0, 0, 1, 0]

# # ],
# # [
# # 	[0, 0, 2/3, 1/3],
# # 	[0, 1, 0, 0],
# # 	[0, 0, 1, 0]
# # ]
# # ])

# # R = P

# # print( np.divide( P, 3 ) )

# import csv

# outcsv=open('./immates.csv','w')
# writer = csv.writer(outcsv)
# writer.writerow(["Train2008-Test2009", "Train2008-Test2010", "Train2009-Test2008", "Train2009-Test2010", "Train2010-Test2008", "Train2010-Test2009"])

# for i in drange(0, 1, 0.1):
#     print (i)

p = { }

def add( a ):
	p[a] = 44
	print( p )

def pp():
	p = {"2": 3}
	add( "44" )

if __name__ == '__main__':
	pp()






