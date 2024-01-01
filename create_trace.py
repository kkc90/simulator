import os
import sys
import time
import numpy as np

def main():
    ##### Setting for TC #####
    bw = 20.0
    with open("1", "w") as f:
        for i in range(0, 300):
            if int(i) % 60 == 0 and int(i) != 0:
                delay = 80
            else:
                delay = 50
            
            data = "%d %f %d\n" % (i, bw, delay)
            f.write(data)

if __name__ == '__main__':
    main()
