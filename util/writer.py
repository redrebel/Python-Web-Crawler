import csv

def saveCSV(data, fileName):
	print("CSV format save : " , fileName)
	with open(fileName, 'w') as f:
		writer = csv.writer(f, delimiter=',')
		for word, freq in data:
			writer.writerow([word, freq])

def saveTxt(data, fileName):
	print("txt format save : " , fileName)
	with open(fileName, 'w') as f:
		for p in data:
			f.write(p+"\n")


#saveCSV(["ss","dd"], "d.csv")