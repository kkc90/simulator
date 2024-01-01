import os
import sys
import time
import random
random.seed(time.time())

# FILE_PATH = "./traces/trace_sample.log";
DIR_PATH = "./traces/train/"

##### Select a trace log #####
# def selectLog():
#     FileList = os.listdir(DIR_PATH)
#     num = random.randint(0, len(FileList)-1)
#     return FileList[num]


##### Funtion to read a file #####
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


def main():
    ##### Setting for TC #####
    NET_INTERFACE = sys.argv[1]



    # wait for chrome to start
    time.sleep(2)

    # init setup
    os.system("ip link add ifb0 type ifb")
    os.system("ip link set dev ifb0 up")
    os.system(f"tc qdisc add dev {NET_INTERFACE} ingress")
    os.system(f"tc filter add dev {NET_INTERFACE} parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0")
    os.system(f"tc qdisc add dev ifb0 root netem delay 50ms rate 1mbit")
    time.sleep(1)

    # rerese char of file name so it sort like: car_1, bus_1, tram_1, car_2, bus_2....
    files = sorted(os.listdir(DIR_PATH), key=lambda x: x[::-1])
    if os.getenv('RANDOM_TRACE'):
        print(f"use random trace file")
        random.shuffle(files)

    while True:
        for FILE in files:
            FILE_PATH = DIR_PATH + FILE;
            NET_INTERFACE  = ""
            TIMESTAMP, THROUGHPUT = fileRead(FILE_PATH)

            # Apply tc to the network interface
            for i in range(0,len(TIMESTAMP)):
                if len(TIMESTAMP) != len(THROUGHPUT):
                    break

                os.system(f"tc qdisc change dev ifb0 root netem delay 50ms rate {THROUGHPUT[i]}mbit")
                os.system(f"tc qdisc show dev ifb0")

                if i != len(TIMESTAMP)-1:
                    time.sleep(float(TIMESTAMP[i+1]) - float(TIMESTAMP[i]))
                else:
                    time.sleep(1)


            time.sleep(1)
            # manually del if needed
            # os.system(COMMAND_DEL)


if __name__ == '__main__':
    main()
