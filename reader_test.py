import numpy as np 
import pandas
import csv
from datetime import datetime

mst_file = '/home/reiti/Documents/PhD/Modell/FlightStatsHAM/ATMAP_ARR_DEP.csv'

dateparse = lambda dates: pandas.datetime.strptime(dates, '%Y-%m-%d')
dataset = pandas.read_csv(mst_file, parse_dates=['Datum'], index_col='Datum',date_parser=dateparse)
dataset.index

print(dataset)

data = []