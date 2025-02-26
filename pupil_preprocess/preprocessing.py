# pupil_preprocess/preprocessing.py
import pandas as pd
import re

def label_by_type(file_list):
    """Classify lines in the file based on content type."""
    lineType = []
    indices = {"empty": [], "comment": [], "sample": [], "events": [], "saccade": [], "blink": [], "fixation": [], "msg": []}
    
    for index, line in enumerate(file_list):
        if len(line) < 3:
            lineType.append("EMPTY")
            indices["empty"].append(index)
        elif line.startswith('*'):
            lineType.append("COMMENT")
            indices["comment"].append(index)
        elif line.split()[0][0].isdigit():
            lineType.append("SAMPLE")
            indices["sample"].append(index)
        else:
            event_type = line.split()[0]
            lineType.append(event_type)
            indices["events"].append(index)
            if event_type in ["SSACC", "ESACC"]:
                indices["saccade"].append(index)
            if event_type in ["SBLINK", "EBLINK"]:
                indices["blink"].append(index)
            if event_type in ["SFIX", "EFIX"]:
                indices["fixation"].append(index)
            if event_type == "MSG":
                indices["msg"].append(index)
    
    return indices

def extract_by_type(data, indices):
    """Extract different types of events from the raw data."""
    sample_df = pd.DataFrame([data[i].split() for i in indices["sample"]], columns=['timestamp', 'left_x', 'left_y', 'left_pupil_size', 'right_x', 'right_y', 'right_pupil_size'])
    blink_df = pd.DataFrame([data[i].split() for i in indices["blink"]], columns=['type', 'eye', 'start_time', 'end_time', 'duration'])
    fixation_df = pd.DataFrame([data[i].split() for i in indices["fixation"]], columns=['type', 'eye', 'start_time', 'end_time', 'duration', 'xAvg', 'yAvg', 'pupilAvg'])
    return sample_df, blink_df, fixation_df

def form_blink_saccade_df_left_right(blink, saccade):
    """Separate blinks and saccades into left and right eye events."""
    left_blink = blink[blink["eye"] == "L"]
    right_blink = blink[blink["eye"] == "R"]
    left_saccade = saccade[saccade["eye"] == "L"]
    right_saccade = saccade[saccade["eye"] == "R"]
    return left_blink, right_blink, left_saccade, right_saccade

def label_saccades_with_blinks(df, side):
    """Label saccades occurring near blinks."""
    label = ["saccade"] * len(df)
    for index, row in df.iterrows():
        if row["type"] == "EBLINK":
            label[index] = f"{side} blink"
    return label

def fixation_information_df(fixation_df):
    """Extract fixation data separately for left and right eye."""
    left_fix = fixation_df[fixation_df["eye"] == "L"]
    right_fix = fixation_df[fixation_df["eye"] == "R"]
    return left_fix, right_fix

def label_in_between(all_events_df, side):
    """Label intermediate timestamps between events."""
    df_intermediates = pd.DataFrame({
        "timestamp": all_events_df["start_time"].tolist() + all_events_df["end_time"].tolist(),
        "label": [f"start {side} event"] * len(all_events_df) + [f"end {side} event"] * len(all_events_df)
    })
    return df_intermediates.groupby("timestamp")["label"].apply(', '.join).reset_index()

def chop_timeseries(head, tail, sample_rate, data, id_name):
    """Segment time series data into predefined windows."""
    data["timestamp"] = pd.to_numeric(data["timestamp"], errors='coerce')
    start = data["timestamp"].min() + head
    end = data["timestamp"].max() - tail
    segment = data[(data["timestamp"] >= start) & (data["timestamp"] <= end)].copy()
    segment["id"] = id_name
    return segment
