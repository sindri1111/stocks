

def momentumPercent(now, then):
    return now/then*100

def momentumAbs(now, then):
    return now-then

def movingAverage(data, n):
    movingaverage = [0 for i in range(n-1, len(data))]
    for i in range(n-1,len(data)):
        movingaverage[i-n+1] = sum(data[i-n+1:i+1])/n
    return movingaverage

def exponentialMovingAverage(data, n, i=-1, smoothing=2):
    if i == -1:
        # First time running
        i = len(data)-n
    print(data[i:i + n])
    if i == 0:
        return sum(data[:n])/n

    return data[i+n-1]*(smoothing/(1+n)) + (1-(smoothing/(1+n)))*exponentialMovingAverage(data,n,i-1)



print(exponentialMovingAverage([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], 5))

