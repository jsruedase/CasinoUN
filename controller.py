import config as cf
import model
import time
import csv
csv.field_size_limit(2147483647)

file = cf.data_dir + "base_datos.csv"
input_file = list(csv.DictReader(open(file, encoding="utf-8")))
