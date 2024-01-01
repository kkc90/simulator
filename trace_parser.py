import csv
import os, sys

BASE_DIR = os.path.dirname(sys.argv[0])

def trace_parse(raw_trace_dir, parsed_trace_dir, type):
    files = sorted(os.listdir(raw_trace_dir))
    for file in files:
        file_path = os.path.join(raw_trace_dir, file)
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)

            parsed_data = []
            idx = 0
            last_ts = None

            # skip several first lines due too warm up
            for _ in range(0, 10): next(reader)
            for row in reader:
                # skip duplicate timestamp
                if row[0] == last_ts: continue
                # the data has mix of 3G, 4G, 5G, only select 5G mode
                if row[6] != type: continue

                throughput_mbps = int(row[12])/1000.0
                parsed_throughput_mbps = 0.2 if throughput_mbps < 0.2 else throughput_mbps
                parsed_data.append(f"{idx} {parsed_throughput_mbps}")

                idx += 1
                last_ts = row[0]

            parsed_data_text = "\n".join(parsed_data)
            with open(os.path.join(parsed_trace_dir, file), 'w') as f:
                f.write(parsed_data_text)

trace_parse(f"{BASE_DIR}/trace_raw/5G/", f"{BASE_DIR}/rootfs/traces/test/5G/", '5G')
trace_parse(f"{BASE_DIR}/trace_raw/4G/", f"{BASE_DIR}/rootfs/traces/test/4G/", 'LTE')
