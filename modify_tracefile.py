import os
import sys
import time

DIR_PATH = "./traces/test_categorized/"
listOfCategories = ['bus', 'car', 'ferry', 'metro', 'mixed', 'stable', 'train', 'tram']

NEW_DIR_PATH = "./traces/test_new/"

##### Function to read a file #####
def fileRead(file_name):
    print(f"Reading file: {file_name}")
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

def fileWrite(file_name, timestamp_list, throughput_list):
    print(f"Writing file: {file_name}")
    f = open(file_name, mode='wt')

    for i in range(0, len(timestamp_list)):
        f.write(str(timestamp_list[i])+'\t'+str(throughput_list[i])+'\n')            
    f.close()
    return file_name


def main():
    for SELECT_DIR in listOfCategories:
        files = sorted(os.listdir(DIR_PATH + SELECT_DIR))
        for file_path in files:
            timestamp, throughput = fileRead(DIR_PATH + SELECT_DIR + "/" + file_path)

            if len(timestamp) != len(throughput):
                break
            
            for i in range(0, len(timestamp)):
                if throughput[i] < 0.3:
                    if i == 0:
                        throughput[i] == 0.3
                    else:
                        throughput[i] == throughput[i-1]
            fileWrite(NEW_DIR_PATH + SELECT_DIR + "/" + file_path, timestamp, throughput)

if __name__ == '__main__':
    main()
