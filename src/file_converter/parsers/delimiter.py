def detect_delimiter(file_path, user_delimiter=None):
    if user_delimiter:
        return user_delimiter
    
    with open(file_path, 'r') as file:
        first_line = file.readline()
        possible_delimiters = [',', ';', '\t', '|']
        delimiter_counts = {delimiter: first_line.count(delimiter) for delimiter in possible_delimiters}
        
    return max(delimiter_counts, key=delimiter_counts.get)

def read_csv_with_delimiter(file_path, delimiter):
    import csv
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=delimiter)
        return list(reader)

def write_csv_with_delimiter(data, file_path, delimiter):
    import csv
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerows(data)