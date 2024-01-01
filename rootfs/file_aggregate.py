import os
import sys
import time

DIR_PATH = "./traces/test/"

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
            if len(temp_arr) > 2 or len(temp_arr) < 1:
                print(f"data format error in line: {line}")
                continue
            timestamp_list.append(float(temp_arr[0]))
            throughput_list.append(float(temp_arr[1]))
            
    f.close()

    return (timestamp_list, throughput_list,)

def main():
    # SELECT_DIR = sys.argv[2]
    SELECT_DIR = "mixed"

    files = sorted(os.listdir(DIR_PATH + SELECT_DIR))
    f = open("trace_aggregate", mode='w')
    new_sec = 0.0
    

    for file_path in files:
        complete_file_path = DIR_PATH + SELECT_DIR + "/" + file_path
        timestamps, throughputs = fileRead(complete_file_path)
        print(f"File {complete_file_path} is read")
        
        ##### Apply tc to the network interface #####
        for i in range(0,len(timestamps)):
            if len(timestamps) != len(throughputs):
                break
            f.write(f"{new_sec} {throughputs[i]}\n")
            new_sec = new_sec + 1.0
            
    f.close()
        # manual del if needed
        # os.system(COMMAND_DEL)


if __name__ == '__main__':
    main()
