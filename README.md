# preprocessing_pupillometry

# Pupil Preprocess Package

## Overview
The `pupil_preprocess` package provides a structured pipeline for preprocessing pupil data. It includes functions for reading raw data, extracting relevant information, filtering signals, and segmenting time-series data for further analysis.

## Installation
To install the package locally, navigate to the root directory and run:
```bash
pip install -e .
```

## Usage
Once installed, you can import the package in your scripts:
```python
from pupil_preprocess import *
```

### Example Workflow
```python
from pupil_preprocess import read_file_line_by_line, label_by_type, extract_by_type

data = read_file_line_by_line("path/to/data", "file.asc")
indices = label_by_type(data)
sample_df, blink_df, fixation_df = extract_by_type(data, indices)
```

## Module Descriptions
### `io.py`
- `read_file_line_by_line(path, file_name)`: Reads a text file line by line.

### `preprocessing.py`
- `label_by_type(file_list)`: Classifies lines based on content type.
- `extract_by_type(data, indices)`: Extracts samples, blink events, and fixations.
- `form_blink_saccade_df_left_right(blink, saccade)`: Separates left and right eye events.
- `label_saccades_with_blinks(df, side)`: Labels saccades occurring near blinks.
- `fixation_information_df(fixation_df)`: Extracts fixation data separately for left and right eye.
- `label_in_between(all_events_df, side)`: Labels intermediate timestamps.
- `chop_timeseries(head, tail, sample_rate, data, id_name)`: Segments time-series data.

### `filtering.py`
- `butter_worth_filter(cutoff_frequency, sampling_frequency, data)`: Applies a Butterworth filter to smooth pupil size data.

### `utils.py`
- `extract_id(i)`: Extracts the participant ID from a filename.

## Author
Developed by Sophie for structured pupil data preprocessing.
