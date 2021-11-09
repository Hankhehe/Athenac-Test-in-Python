import csv


class FileInput:
    def UrlList():
        with open('testurl.csv', newline='') as csvfile:
            data = list()
            rows = csv.reader(csvfile)
            for row in rows:
                data.append(row[0])
            return data
