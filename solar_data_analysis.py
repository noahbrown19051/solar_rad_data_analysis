import sys
from numpy import NaN, Inf, arange, isscalar, asarray, array
import pandas as pd
import time
import datetime
import numpy as np
from matplotlib.pyplot import plot, scatter, show
from os import walk
import os



def findMaxInDay(timestamps, intensities):
    '''finds maximum intensity of each day
    returns list of max intensities and timestamps for each max intensity
    '''

    # initializing variables
    lastDay = timestamps[0][3:5]
    
    maxIntensities = []
    maxTimestamps = []
    maxInten = 0 
    maxTime = ''

    # finding max value for each day
    for timestamp, intensity in zip(timestamps, intensities):
        
        day = timestamp[3:5]
        
        if lastDay != day:
            maxIntensities.append(maxInten)
            maxTimestamps.append(maxTime)
            maxInten = intensity
            maxTime = timestamp
        else:
            if intensity > maxInten:
                maxInten = intensity
                maxTime = timestamp
        lastDay = day
    return maxTimestamps, maxIntensities
def findAveInDay(timestamps, intensities):
    '''finds average intensity of each day
    '''
    # initializing variables
    lastDay = timestamps[0][3:5]
    count = 1
    days = []
    aveIntensities = []
    sumIntense = 0 
    lastDate = ''
    for timestamp, intensity in zip(timestamps, intensities):
        day = timestamp[3:5]
        
        if lastDay != day:
            days.append(lastDate)
            aveIntensities.append(sumIntense / count)
        
            count = 0
            sumIntense = 0
            if intensity > 0:
                count += 1
                sumIntense = intensity
        else:
            if intensity > 0:
                count += 1
                sumIntense += intensity
                
        lastDay = day
        lastDate = timestamp[:11] + ' 12:00'

    return days, aveIntensities

def datetimeToEpoch(df):
    # converts timestamp in format '%m/%d/%Y %H:%M' to time in seconds from 1970
    # input of column df of timestamps returns as list of epoch time
    pattern = '%m/%d/%Y %H:%M'

    epochTimes = np.zeros([len(df.index),1], dtype=int)
    idx = 0
    for timestamp in df.values.tolist():
        epochTime = int(time.mktime(time.strptime(timestamp, pattern)))
        epochTimes[idx]= epochTime
        idx += 1
    
    return epochTimes

def epochToDatetime(df):
    # converts epoch time since 1970 to datetime of mountain
    datetimes = []
    for epoch in df.values.tolist():
        readable = datetime.datetime.fromtimestamp(epoch).isoformat()
        print(str(readable))
        datetimes.append(str(readable))
    return datetimes

def analyzeData(path, filename):
    '''creates csv files of mean value and max value
    for each day'''
    df = pd.read_csv(path + '/data/' + filename)
    
    intensity = df['parameterValue'].tolist()
    timestamps = df['timestamp'].tolist()

    # converting timestamp to epoch
    epochTimes = datetimeToEpoch(df['timestamp'])
    
    epochTimes_list = epochTimes.tolist()
    
    maxTimes, maxIntensities = findMaxInDay(timestamps, intensity)
    print(maxTimes)
    maxTimesdf = pd.DataFrame(maxTimes, columns=['timestamp'])

    days, aveIntensities = findAveInDay(timestamps, intensity)
    print(days)
    daysdf = pd.DataFrame(days, columns=['timestamp'])
    daysEpoch = datetimeToEpoch(daysdf['timestamp']).tolist()
    print(daysEpoch)
    maxTimesEpoch = datetimeToEpoch(maxTimesdf['timestamp']).tolist()
    

    # ------------------------------ Sending to .csv ----------------------------- #

    df_averages = pd.DataFrame(list(zip(daysEpoch, days, aveIntensities)), 
                                columns=['unix timestamp', 'timestamp', 'mean intensity'])
    averages_filename = 'daily_mean_' + filename[:-4] + '.csv'
    df_averages.to_csv(path+'/means/'+averages_filename, index=False)

    df_maxs = pd.DataFrame(list(zip(maxTimesEpoch, maxTimes, maxIntensities)),
                            columns=['unix timestamp', 'timestamp', 'max intensity'])
    highs_filename = 'daily_highs_' + filename[:-4] + '.csv'
    df_averages.to_csv(path+'/highs/'+highs_filename, index=False)
    
    

    # --------------------------------- Plotting --------------------------------- #
    # plot(epochTimes, intensity)
    # scatter(maxTimesEpoch, maxIntensities, color='green')
    # scatter(daysEpoch, aveIntensities, color='purple')
    # # scatter(daysEpoch, ar_smoke/max(ar_smoke), color='orange')

    show()



def main():
    cwd = os.getcwd()
    filenames = next(walk(cwd +'/data'), (None, None, []))[2]

    for filename in filenames:
        analyzeData(cwd, filename)

if __name__=="__main__":
    
    main()
    