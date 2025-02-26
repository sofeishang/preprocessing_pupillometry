# pupil_preprocess/utils.py
def extract_id(i):
    import re
    return re.sub(r'^.*?_', '', i)