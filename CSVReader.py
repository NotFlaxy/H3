import pandas as pd

def csv_reader():
    csvFile = pd.read_csv('inputlist.csv')
    print(csvFile)

csv_reader()