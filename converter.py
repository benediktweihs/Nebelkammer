import csv
import sys
#convert nimmt ein txt file mit vorgegebener Struktur und gibt eine Matrix zurück
def convert(file_name,format,delimiter):
    file = ".\\Rohdaten\\" + file_name + "." + format
    #Multidimensionales array -> enthält am Ende alle Daten
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)
        for rowNum, row in enumerate(csv_reader):
            if rowNum == 0:
                #also keine Tabs in den Überschriften verwenden!
                column_count = len(row)
                arr = [[] * 1 for i in range(column_count)]
            elif rowNum != 0:
                for i in range(column_count):
                    arr[i].append(row[i].replace(',','.'))
            else:
                arr = "File korrupt"
    return arr