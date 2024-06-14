# feature_engineering.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from geopy.distance import geodesic

def load_data(nb_path, wb_path):
    df_nb = pd.read_csv(nb_path)
    df_wb = pd.read_csv(wb_path)
    return df_nb, df_wb

def add_datetime_features(df):
    df['Trip Start Time'] = pd.to_datetime(df['Trip Start Time'])
    df['Trip End Time'] = pd.to_datetime(df['Trip End Time'])
    df['start_hour'] = df['Trip Start Time'].dt.hour
    df['start_day'] = df['Trip Start Time'].dt.dayofweek
    df['end_hour'] = df['Trip End Time'].dt.hour
    df['end_day'] = df['Trip End Time'].dt.dayofweek

def calculate_trip_duration(df):
    df['trip_duration'] = (df['Trip End Time'] - df['Trip Start Time']).dt.total_seconds() / 60

def calculate_distance(origin, destination):
    try:
        return geodesic(origin, destination).kilometers
    except:
        return np.nan

def add_distance_feature(df):
    df['distance'] = df.apply(lambda row: calculate_distance(row['Trip Origin'], row['Trip Destination']), axis=1)

def impute_missing_values(df):
    df['Trip Start Time'].fillna(method='ffill', inplace=True)
    df['Trip End Time'].fillna(method='bfill', inplace=True)
    df['missing_trip_start_time'] = df['Trip Start Time'].isnull().astype(int)
    df['missing_trip_end_time'] = df['Trip End Time'].isnull().astype(int)

def encode_driver_action(df):
    label_encoder = LabelEncoder()
    df['driver_action_encoded'] = label_encoder.fit_transform(df['driver_action'])

def cluster_locations(df):
    coords = df[['Trip Origin', 'Trip Destination']].values
    kmeans = KMeans(n_clusters=5, random_state=0).fit(coords)
    df['location_cluster'] = kmeans.labels_

def save_cleaned_data(df_nb, df_wb):
    df_nb.to_csv('nb_cleaned.csv', index=False)
    df_wb.to_csv('wb_cleaned.csv', index=False)

def run_feature_engineering(nb_path, wb_path):
    df_nb, df_wb = load_data(nb_path, wb_path)
    add_datetime_features(df_nb)
    calculate_trip_duration(df_nb)
    add_distance_feature(df_nb)
    impute_missing_values(df_nb)
    encode_driver_action(df_wb)
    cluster_locations(df_nb)
    save_cleaned_data(df_nb, df_wb)

if __name__ == "__main__":
    run_feature_engineering('nb.csv', 'wb.csv')
