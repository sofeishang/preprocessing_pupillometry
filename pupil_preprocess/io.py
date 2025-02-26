# pupil_preprocess/io.py
def read_file_line_by_line(path, file_name):
    with open(path + file_name, "r") as f:
        data = f.read().splitlines(True)
    return data
