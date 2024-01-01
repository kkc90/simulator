import csv
import os, sys

FILE_NAME = "5g_data.csv"
SAVE_DIR = "new_5G"

def trace_parse(raw_trace, parsed_trace):
    with open(raw_trace, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)

        parsed_data = []
        # skip several first lines due too warm up
        # for _ in range(0, 10): next(reader)

        data_idx = 1

        # for row in reader:
        #     print(row)

        for _ in range(0, 1): 
            next(reader)

        for row in reader:
            if int(row[4]) == data_idx:
                throughput_mbps = float(row[6])
                clipped_throughput_mbps = 0.2 if throughput_mbps < 0.2 else throughput_mbps
                parsed_data.append(f"{row[5]} {clipped_throughput_mbps}\n")

            else:
                with open("./"+parsed_trace+"/"+str(data_idx), 'w') as f:
                    for line in parsed_data:
                        f.write(line)

                data_idx += 1
                parsed_data = []

                throughput_mbps = float(row[6])
                clipped_throughput_mbps = 0.2 if throughput_mbps < 0.2 else throughput_mbps
                parsed_data.append(f"{row[5]} {clipped_throughput_mbps}\n")

        with open("./"+parsed_trace+"/"+str(data_idx), 'w') as f:
            for line in parsed_data:
                f.write(line)

trace_parse(FILE_NAME, SAVE_DIR)
