# pupil_preprocess/filtering.py
def butter_worth_filter(cutoff_frequency, sampling_frequency, data):
    from scipy import signal
    z, p, k = signal.butter(1, cutoff_frequency / (sampling_frequency), btype='low', analog=False, output='zpk')
    sos = signal.zpk2sos(z, p, k)
    filtered_data = signal.sosfilt(sos, data)
    return filtered_data