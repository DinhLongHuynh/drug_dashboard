import os 
import sys
sys.path.append(os.path.abspath('../'))
from utils.data_fetcher import fda_downloader, unziper, csv_converter
from utils.data_processor import DataProcessor

# Run:
if __name__ == "__main__":
    fda_downloader()
    unziper(file_path='../data_raw/fda_data_raw.zip',export_path='../data_raw')
    csv_converter(file_path='../data_raw',export_path='../data_csv')
    processor = DataProcessor(data_file='Products_draft.csv')
    processor.smile_generator()
    processor.smile_standardizer()
    processor.get_properties()
    processor.export()

