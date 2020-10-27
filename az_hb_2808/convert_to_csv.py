import sys
import re
import csv

columns = [
    "crime",
    "admissions",
    "releases",
    "total"
]

def format_crime(crime):
    crime = crime.replace('/', ' or ')
    crime = crime.replace('.', '')
    crime = crime.lower()
    crime = crime.replace(' ', '_')

    return crime

def parse_data(data):
    data = data.replace(',', '')
    all = data.split(' ')
    return [all[2], all[5], all[8]]

def parse_file(file_name, output_file_name):
    input_file = open(file_name, 'r')
    name = file_name.split('.')[0]
    with open(output_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for line in input_file.readlines():
            line = line.split('\n')[0]
            m = re.search(r"\d", line)
            split_index = m.start()
            raw_crime = line[:split_index - 1]
            crime = format_crime(raw_crime)
            data = line[split_index:]
            writer.writerow([crime] + parse_data(data))


def main():
    file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    parse_file(file_name, output_file_name)

if __name__ == "__main__":
    main()
