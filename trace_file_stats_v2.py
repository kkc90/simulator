import os
import sys
import time
import numpy as np

# DIR_PATH = "./rootfs/traces/test/"
DIR_PATH = "./rootfs/traces/"

##### Function to read a file #####
def fileRead(file_name):
    # print(f"Reading file: {file_name}")
    f = open(file_name, mode='rt')

    temp_arr = list()
    timestamp_list = list()
    throughput_list = list()

    while True:
        line = f.readline()
        if not line:
            break
        else:
            line = line.strip('\n')
            temp_arr = line.split()
            if len(temp_arr) != 2:
                print(f"data format error in line: {line}")
                continue
            timestamp_list.append(float(temp_arr[0]))
            throughput_list.append(float(temp_arr[1]))

    return (timestamp_list, throughput_list)

def main():
    ##### Setting for TC #####
    # for select_dir in ['mixed', '4G', 'oboe']:
    for select_dir in ['train']:
        all_throughput = []

        files = sorted(os.listdir(DIR_PATH + select_dir))


        for file_path in files:
            timestamp, throughput = fileRead(DIR_PATH + select_dir + "/" + file_path)
            all_throughput.extend(throughput)

        print(f"{select_dir}: {round(np.average(all_throughput), 2)}, {round(np.std(all_throughput), 2)}, {round(np.std(all_throughput)/np.average(all_throughput), 2)}")
        print(f"{select_dir}: {min(all_throughput)}, {max(all_throughput)}")

if __name__ == '__main__':
    main()
