import csv
from math import sqrt
from decimal import Decimal

def get_xoutliers(distances, avg_distance):
	xoutlier = list()
	for i in range(len(distances)):
		if distances[i][1] > avg_distance * Decimal('2.5'):
			xoutlier.append(distances[i][0])
	return xoutlier

def get_youtliers(distances, avg_distance):
	youtlier = list()
	for i in range(len(distances)):
		if distances[i][1] > avg_distance * Decimal('2.5'):
			youtlier.append(distances[i][0])
	return youtlier

def get_outliers(xout, yout):
	out = list()
	for i in range(len(xout)):
		for j in range(len(yout)):
			if xout[i] == yout[j]:
				out.append(xout[i])
	return out

def print_table(xAvg, yAvg, out):
	dash = '-' * 90
	val1 = out and str(out[0]) or "Nil"
	if armValue == 1:
		print(dash)
		print('{:<10s}{:>20s}{:>20s}{:>12s}'.format("Arm No","X Axis Average", "Y Axis Average", "Outliers"))
	print(dash)
	print('{:<10d}{:>15.5f}{:>20.5f}{:>30}'.format(armValue,xAvg,yAvg,val1))
	new = out[1:]
	for i in range(len(new)):
		print('{:>75}'.format(new[i]))

def maxtomin(matrix, axis):
	matrix.sort(key=lambda x: x[axis], reverse=True)

def get_sorted_neighbor(train):
	#sort on X axis which is 0
	maxtomin(train, 0)
	x_distances = list()
	y_distances = list()
	dec = Decimal('0.0')
	xDistance = dec
	xDistance1 = dec
	yDistance = dec
	yDistance1 = dec
	totalXDist = dec
	totalYDist = dec
	for i in range(len(train)):
		#calculate distance for last item
		if (i+1 >= len(train)):
			xDistance = Decimal(str(train[i-1][0] - train[i][0]))
		#calculate distance for all item in forward way
		else:
			xDistance = Decimal(str(train[i][0] - train[i+1][0]))

		#calculate distance for all item in backward way
		if (i-1 > 0):
			xDistance1 = Decimal(str(train[i-1][0] - train[i][0]))
		#calculate distance for first item
		else:
			xDistance1 = xDistance
		#minimum of b->a , b->c add all shortest distances
		totalXDist += min(xDistance, xDistance1)
		x_distances.append((train[i], min(xDistance, xDistance1)))
	x_distances.sort(key=lambda tup: tup[1])
	#calculate xAxis Average
	xAvg = totalXDist/len(x_distances)
	xout = get_xoutliers(x_distances, xAvg)

	#like X followed same calculations for Y
	maxtomin(train, 1)
	for i in range(len(train)):
		if (i+1 >= len(train)):
			yDistance = Decimal(str(train[i-1][1] - train[i][1]))
		else:
			yDistance = Decimal(str(train[i][1] - train[i+1][1]))

		if (i-1 > 0):
			yDistance1 = Decimal(str(train[i-1][1] - train[i][1]))
		else:
			yDistance1 = yDistance
		totalYDist += min(yDistance, yDistance1)
		y_distances.append((train[i], min(yDistance, yDistance1)))
	y_distances.sort(key=lambda tup: tup[1])
	yAvg = totalYDist/len(y_distances)
	yout = get_youtliers(y_distances, yAvg)
	outliers = get_outliers(xout, yout)
	print_table(xAvg, yAvg, outliers)

def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())

def str_column_to_int(dataset, column):
	for row in dataset:
		row[column] = int(row[column].strip())

def load_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = csv.reader(file)
		for row in csv_reader:
			dataset.append(row)
	return dataset

testArray = load_csv('Sample_Data.csv')

for i in range(len(testArray[0])-1):
	str_column_to_float(testArray, i)
str_column_to_int(testArray, 2)

armValue = 1
index = 0

for i in range(len(testArray)):
	if armValue != testArray[i][2]:
		get_sorted_neighbor(testArray[index:i])
		index = i
	elif i == len(testArray)-1:
		get_sorted_neighbor(testArray[index:i+1])
	armValue = testArray[i][2]
