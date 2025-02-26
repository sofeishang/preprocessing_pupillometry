import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import warnings
import pingouin as pg
from pupil_preprocess import (
    read_file_line_by_line, label_by_type, extract_by_type, 
    form_blink_saccade_df_left_right, label_saccades_with_blinks, 
    fixation_information_df, label_in_between, chop_timeseries,
    butter_worth_filter, extract_id
)

# Configure settings
pd.set_option('display.max_columns', 300)
pd.set_option('display.max_rows', None)
warnings.filterwarnings('ignore')
sns.set_palette("cubehelix")

# Define paths
data_path = "/Users/sophies/Desktop/Project_Analysis/Project_2/behavioral/"
data_file = "cleaned_data_updated_CB_previous_angle.csv"
participant_data = pd.read_csv(data_path + data_file)

project_path = "/Users/sophies/Desktop/Project_Analysis/Project_2_Data"
export_path = "/Users/sophies/Desktop/Project_Analysis/Project_2/pupillometry/"

# Retrieve and filter participant folders
folders = [f for f in os.listdir(project_path) if not f.startswith(".")]
interested_lst, missing_lst = [], []
trial_info_list = ["TRIALID", "prediction:", "played", "OUTCOME", "outcome:", "outcome", "jitter", "Trial"]

# Process each participant
for folder in folders:
    print(f"Processing participant: {folder}")
    sub_folder_path = os.path.join(project_path, folder)
    behavioral_files = os.listdir(sub_folder_path)
    participant_id = extract_id(folder)
    participant_data_subset = participant_data[participant_data.id == int(participant_id)]
    
    for file in behavioral_files:
        if file.endswith(".asc"):
            data = read_file_line_by_line(sub_folder_path, file)
            labeled_indices = label_by_type(data)
            
            sample_df, blink_df, fixation_df = extract_by_type(data, labeled_indices)
            left_blink, right_blink, left_saccade, right_saccade = form_blink_saccade_df_left_right(blink_df, fixation_df)
            
            left_blink["left_eye_label"] = label_saccades_with_blinks(left_blink, "left")
            right_blink["right_eye_label"] = label_saccades_with_blinks(right_blink, "right")
            left_fix, right_fix = fixation_information_df(fixation_df)
            
            left_events = pd.concat([left_blink, left_fix])
            right_events = pd.concat([right_blink, right_fix])
            left_labeled = label_in_between(left_events, "left")
            right_labeled = label_in_between(right_events, "right")
            
            all_labeled = pd.merge(left_labeled, right_labeled, on="timestamp")
            df_merged = chop_timeseries(2000, 5000, 2, sample_df, participant_id)
            
            # Apply Butterworth filter
            df_merged["filtered_pupil_size"] = butter_worth_filter(3.75, 250, df_merged["left_pupil_size"]) 
            
            # Save processed data
            output_file = os.path.join(export_path, f"{folder}_processed.csv")
            df_merged.to_csv(output_file, index=False)
            print(f"Saved processed data for {folder} to {output_file}")
