#!/usr/bin/env python3
#https://github.com/mw18f/BCH4885.git

#read a file
def findpeak(x):
    import numpy as np
    from matplotlib import pyplot
    f=open(x,'r')
    lines=f.readlines()
    f.close()
##put time and absirbance into list named times and list named heights
    times=[]
    heights=[]
    for line in lines[3:]:
        words=line.split()
        if len(words)>1:
            times.append(float(words[0]))
            heights.append(float(words[1]))
##open a list for the time and absorbance of start and end of a peak, p = peak number 
    res_time=[]
    res_height=[]
    p=0
    i=1
    while i+1< len(times):
#set a threshould 40 for looking for start point of the peak, from start point adding following points to the list
        while heights[i]> 40:    
            res_time.append(times[i])
            res_height.append(heights[i])
           
#when the point arrive at minmum value, this point is end point of the peak                  
            if heights[i-1]>heights[i] and heights[i]<heights[i+1] :
                p+=1
             
##in this list, the first one is begin of a peak, the last one is end of a peak
 
                begin=res_time[0]
                end=res_time[-1]
##the max point between start and end point is peak point 
                a = np.where(res_height==np.max(res_height))
                peaktime = res_time[a[0][0]]
                peakab = res_height[a[0][0]]
                pyplot.plot(begin,res_height[0],'ro')
                pyplot.plot(end,res_height[-1],'ro')
                pyplot.plot(peaktime,peakab,'go')
##print output using format string
                print("peak %d starts at %.3f, end at %.3f, peak point at time %.3f with absorbance %.3f" %((p),begin,end,peaktime,peakab))
#go to the next peak
                res_time = []
                res_height=[]
                break
            i+=1
        i+=1
# plot 

    pyplot.plot(times,heights)
    pyplot.show()

findpeak("superose6_50.asc")
