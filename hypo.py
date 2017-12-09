def factorial( n ):
	res = 1;
	for i in range( 1, n + 1 ):
		res = res * i
	return res

def oneIter( i, p ):
	return ( factorial( 150 ) / ( factorial( i ) * factorial( 150 - i ) ) ) * ( p ** i ) * ( ( 1 - p ) ** ( 150 - i ) )

def getPValue( m, p ):
	sum = 0
	for i in range( m + 1, 151 ):
		sum = sum + oneIter( i, p )
	return sum 

# print( factorial(3) )
# print( oneIter( 88, 0.5 ) )

print( getPValue( 0, 0.5 ))



# print( 2/ 3)