

def momentumPercent(now, then):
    return now/then*100

def momentumAbs(now, then):
    return now-then

def movingAverage(data, n):
    movingaverage = [0 for i in range(n-1, len(data))]
    for i in range(n-1,len(data)):
        movingaverage[i-n+1] = sum(data[i-n+1:i+1])/n
    return movingaverage

def movingAverage2(data, n):
    movingaverage = [0 for i in range(len(data))]
    for i in range(len(data)):
        if i < n-1:
            movingaverage[i] = sum(data[:i+1])/len(data[:i+1])
        else:
            movingaverage[i] = sum(data[i - n + 1:i + 1]) / n
    return movingaverage


def exponentialMovingAverageRecursion(data, n, i=-1, smoothing=2):
    if i == -1:
        # First time running
        i = len(data)-n
    if i == 0:
        return sum(data[:n])/n

    return data[i+n-1]*(smoothing/(1+n)) + (1-(smoothing/(1+n)))*exponentialMovingAverage(data,n,i-1)

def exponentialMovingAverage(data, n, smoothing=2):
    ret = [0 for i in range(len(data)-n+1)]
    ret[0] = sum(data[:n])/n
    for i in range(1,len(ret)):
        ret[i] = data[i+n-1]*(smoothing/(1+n)) + (1-(smoothing/(1+n)))*ret[i-1]
    return ret

def exponentialMovingAverage2(data, n, smoothing=2):
    ret = [0 for i in range(len(data))]
    ret[0] = data[0]
    for i in range(1,len(ret)):
        ret[i] = data[i]*(smoothing/(1+n)) + (1-(smoothing/(1+n)))*ret[i-1]
    return ret

