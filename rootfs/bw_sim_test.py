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
    delay_list = list()

    while True:
        line = f.readline()
        if not line:
            break
        else:
            line = line.strip('\n')
            temp_arr = line.split()
            if len(temp_arr) > 3 or len(temp_arr) < 1:
                print(f"data format error in line: {line}")
                continue
            timestamp_list.append(float(temp_arr[0]))
            throughput_list.append(float(temp_arr[1]))
            if len(temp_arr) == 3:
                delay_list.append(float(temp_arr[2]))

    return (timestamp_list, throughput_list, delay_list)

def main():
    ##### Setting for TC #####
    NET_INTERFACE = sys.argv[1]
    SELECT_DIR = sys.argv[2]
    DEFAULT_DELAY = sys.argv[3]

    files = sorted(os.listdir(DIR_PATH + SELECT_DIR))

    # init setup
    os.system("ip link add ifb0 type ifb")
    os.system("ip link set dev ifb0 up")
    os.system(f"tc qdisc add dev {NET_INTERFACE} ingress")
    os.system(f"tc filter add dev {NET_INTERFACE} parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0")
    os.system(f"tc qdisc add dev ifb0 root netem delay 20ms rate 1mbit")
    time.sleep(1)

    while True:
        for file_path in files:
            complete_file_path = DIR_PATH + SELECT_DIR + "/" + file_path
            timestamps, throughputs, delays = fileRead(complete_file_path)
            print(f"File {complete_file_path} is read")
            use_delay = False
            if len(delays) == len(timestamps):
                use_delay = True
                print("Delay emulation is applied")

            ##### Apply tc to the network interface #####
            for i in range(0,len(timestamps)):
                if len(timestamps) != len(throughputs):
                    break

                delay = DEFAULT_DELAY if not use_delay else delays[i]
                os.system(f"tc qdisc change dev ifb0 root netem delay {delay}ms rate {throughputs[i]}mbit")
                os.system(f"tc qdisc show dev ifb0")

                if i != len(timestamps)-1:
                    time.sleep(float(timestamps[i+1]) - float(timestamps[i]))
                else:
                    time.sleep(1)

            # manual del if needed
            # os.system(COMMAND_DEL)


if __name__ == '__main__':
    main()
