

import pandas as pd
import os

def load_raw_data(filename):
    """
    Load data from the data/raw folder.
    
    Args:
        filename (str): The name of the file to load.
        
    Returns:
        DataFrame: The loaded data.
    """
    # Construct the path to the raw data file
    file_path = os.path.join(os.path.dirname(__file__), '../../data/raw', filename)
    
    # Load the data
    df = pd.read_csv(file_path)
    
    return df

def load_raw_data_location(filename):


 # Construct the path to the raw data file
    file_path = os.path.join(os.path.dirname(__file__), '../../data/raw', filename)
    
    # Load the data
    df2 = pd.read_csv(file_path)
    
    return df2