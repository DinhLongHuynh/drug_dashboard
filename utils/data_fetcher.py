import os 
import pandas as pd
import zipfile
import requests
import time
from tqdm import tqdm
import pubchempy as pcp

# Module 1: Downloader
def fda_downloader(file_path="../data_raw/fda_data_raw.zip", url="https://www.fda.gov/media/89850/download"):
    '''A function to download data from FDA@Drug website and store to desire file_path.
    
    Parameters:
    ----------
    file_path (zip file): a place to store donwloaded zip file.
    url (http): an url leads to download page of FDA@Drug.'''
    
    # Mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, stream=True)

    # Check if request was successful
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Download complete: {file_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")




# Module 2: Unziper
def unziper(file_path,export_path):
    '''A function to unzip .zip file and delete original .zip file after unzip.
    
    Parameters:
    ----------
    file_path (zip file): a path to zip file.
    export_path (dir): a place to store unzip files.'''

    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(export_path)
        os.remove(file_path)
    except Exception as e:
        print(f'An error occurred: {e}')


# Module 3: Converter
def csv_converter(file_path='../data_raw',export_path='../data_csv'):
    '''A function to convert txt file to csv file give a file path.
    
    Parameters:
    ----------
    file_path (txt file or dir): if txt file, the function converts only 1 file. if dir path, the function converts every .txt file in the directory.
    export_path (dir): a place to store converted csv files.'''

    if os.path.isdir(file_path):
        file_names = os.listdir(file_path)
        for file in file_names:
            try: 
                df = pd.read_csv(file_path+'/'+file, on_bad_lines='skip', sep = '\t',encoding='ISO-8859-1')
                new_file_name = file.split('.')[0]+'.csv'
                df.to_csv(f"{export_path}/{new_file_name}",index=False)
            except Exception as e:
                print(f"An error occurred: {e}")
        print(f'All the files have been converted, please check {os.path.abspath(export_path)}')
    
    elif os.path.isfile(file_path):
        try:
            file = file_path.split('/')[-1]
            df = pd.read_csv(file_path, on_bad_lines='skip', sep = '\t',encoding='ISO-8859-1')
            new_file_name = file.split('.')[0]+'.csv'
            df.to_csv(f"{export_path}/{new_file_name}",index=False)
            print(f'{file} has been converted, please check {os.path.abspath(export_path)}')
        except Exception as e:
                print(f"An error occurred: {e}")

    else:
        raise FileNotFoundError(f"Error: The specified path '{file_path}' does not exist.")


# Module 4: Difference Analyzer


# Module 5: Update the new/updated records


# Module 6: Push to database




