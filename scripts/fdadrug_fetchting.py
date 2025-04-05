import os 
import sys
sys.path.append(os.path.abspath('../'))
from utils.data_fetcher import fda_downloader, unziper, csv_converter
from utils.data_processor import smile_generator

# Run:
if __name__ == "__main__":
    fda_downloader()
    unziper(file_path='../data_raw/fda_data_raw.zip',export_path='../data_raw')
    csv_converter(file_path='../data_raw',export_path='../data_csv')
    smile_generator(data_path="../data_csv",data_file='Products.csv')
