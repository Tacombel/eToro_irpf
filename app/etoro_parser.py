import os

if __name__ == '__main__':

    for f in os.walk(./):
        for file in f[2]:
            if '.xls' in file:
