import struct
import csv
import glob

def to_float(s):
    b=[]
    for i in range(0,4):
        b+=[int(s[2*i:2*i+2],16)]
    b=struct.pack('4B', *b)
    return struct.unpack('>f', b)[0]

def format_time(t):
    hour=int(t[0:2])
    minute=int(t[3:5])
    second=int(t[6:8])
    millis=int(t[9:15])//1000
    return '{0}:{1}:{2}.{3}'.format(hour, minute, second, millis)
time=0
rpm=0
volt=0
curr=0
power=0
accel=0
#f1 = open('2016_10_15_14_12_11.log', 'r')
#csvfile = open('coast1.csv', 'w')

#Parses through the files indicated through the path.
def data_parser(path):
    path += '*.log'
    files = glob.glob(path)
    csvfile = open('road_test_data.csv', 'w')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['time', 'rpm', 'mph', 'voltage', 'current', 'power', 'accel pedal'])
    index = 0
    total = 0
    frequency = 10 # record every nth line
    for file in files:
    f1 = open(file, 'r')
    print(file)
    index2 = 0
    freq_index = 0
    for l in f1.readlines():
        if l[0]=='#' or l[0:4]=='2016':
            continue
        t=l.split(';')
        if len(t) < 2:
            continue
        if t[1] == '0x310':
            rpm=to_float(t[2][2:])
            mph=rpm*60*3.1415*21/12/5280
            time=format_time(t[0])
            #if t[0]>'14_20_55_000000' and t[0]<'14_23_00_000000':
            if freq_index == frequency:
                csvwriter.writerow([time,rpm,mph,volt,curr,power,accel])
                freq_index = 0
                total+=1
            else:
                freq_index+=1
                continue
        elif t[1] == '0x123':
            volt=to_float(t[2][2:])
            power=curr*volt
        elif t[1] == '0x124':
            curr=to_float(t[2][2:])
            power=curr*volt
        elif t[1] == '0x282':
            accel=to_float(t[2][10:])
    f1.close()
    index+=1
    print(str(total) + " lines")
    print(str(index) + " files")

data_parser('/home/matthew/Desktop/CALSOL/vacaville_datalogger_files/')
