import time


start = time.time()
filenames = ['file1.txt', 'CommonSpeak_Bruted.txt']
with open('merged.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())
stop = time.time()
print(str(stop-start))