import csv

class ImportDataByFile:
    def ImportCSV(self,filepath:str)->list:
        with open(filepath, newline='') as csvfile:
            data = list()
            rows = csv.reader(csvfile)
            for row in rows:
                data.append(row[0])
            return data
