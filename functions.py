import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def summary_statistics(dataset):
    return (dataset.count(),dataset.dtypes, dataset.describe(), dataset.shape)

def find_and_remove_duplicates(dataset, dataset_name="Dataset"):
    total_before = len(dataset)
    duplicates = dataset[dataset.duplicated()]
    num_duplicates = len(duplicates)
    
    print(f"{dataset_name} - Total Rows Before Cleaning: {total_before}")
    print(f"{dataset_name} - Duplicate Rows Found: {num_duplicates}")
    
    dataset_cleaned = dataset.drop_duplicates().reset_index(drop=True)
    total_after = len(dataset_cleaned)
    
    print(f"{dataset_name} - Total Rows After Removing Duplicates: {total_after}")
    return dataset_cleaned

def to_number(dataset,field_names):
    for field in field_names:
        dataset[field] = pd.to_numeric(dataset[field], errors='coerce')
    return dataset[field]
    
def remove_outliers(dataset, fields, lower_bound=0.01, upper_bound=0.99, plot=False):
    for field in fields:
        if plot:
            plt.figure(figsize=(4, 2))
            dataset.boxplot(column=[field])
            plt.title(f"Before: {field}")
            plt.grid(False)
            plt.show()

        Q1, Q3 = dataset[field].quantile([lower_bound, upper_bound])
        median = dataset[field].median()
        print(f"{field} - Lower ({lower_bound*100}%): {Q1}, Upper ({upper_bound*100}%): {Q3}")

        dataset.loc[dataset[field] < Q1, field] = np.nan
        dataset.loc[dataset[field] > Q3, field] = np.nan
        dataset[field].fillna(median, inplace=True)

        if plot:
            plt.figure(figsize=(4, 2))
            dataset.boxplot(column=[field])
            plt.title(f"After: {field}")
            plt.grid(False)
            plt.show()

    return dataset

def clean_nan_data(dataset):
    # Get columns with missing values
    null_counts = dataset.isnull().sum()
    null_cols = null_counts[null_counts > 0].index

    # Track changes
    summary = []

    for col in null_cols:
        if dataset[col].dtype == 'object':
            before = dataset.shape[0]
            dataset = dataset[dataset[col].notnull()]  # Drop rows with null object fields
            after = dataset.shape[0]
            summary.append(f"Dropped {before - after} rows due to nulls in object column '{col}'.")
        else:
            median = dataset[col].median()
            nulls = dataset[col].isnull().sum()
            dataset[col].fillna(median, inplace=True)
            summary.append(f"Filled {nulls} nulls in numeric column '{col}' with median value {median}.")

    return dataset, summary

# Used to convert arr_delay and dep_Delays into costs
def delay_costs(delay):
    if delay > 15:
        delay_costs = (delay - 15) * 75
    else:
        delay_costs = 0
    return delay_costs

#Calculates the airport cost based on the airport type.
def airport_costs(type):
    if type == 'medium_airport':
        airport_costs = 5000
    elif type == 'large_airport':
        airport_costs = 10000
    else:
        airport_costs = 0
    return airport_costs

# Converts miles into dollars
def costs_per_mile(miles):
    return miles*(1.18+8)

# Converts occupancy into number of passengers for one-way flight
def number_of_passengers(occ_rate):
    return (200 * occ_rate)  
                   