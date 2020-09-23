#!/usr/bin/env pyhton3
import math
point_A,point_B,point_C = input("A,B,C coordinate is\ninput with dot seperated: ")   
    
a=math.sqrt((point_B[0]-point_C[0])*(point_B[0]-point_C[0])+(point_B[1]-point_C[1])*(point_B[1] - point_C[1]))
b=math.sqrt((point_A[0]-point_C[0])*(point_A[0]-point_C[0])+(point_A[1]-point_C[1])*(point_A[1] - point_C[1]))
c=math.sqrt((point_A[0]-point_B[0])*(point_A[0]-point_B[0])+(point_A[1]-point_B[1])*(point_A[1]-point_B[1]))
alpha=math.degrees(math.acos((a*a-b*b-c*c)/(-2*b*c)))
beta=math.degrees(math.acos((b*b-a*a-c*c)/(-2*a*c)))
gamma=math.degrees(math.acos((c*c-a*a-b*b)/(-2*a*b)))
print alpha
print beta
print gamma