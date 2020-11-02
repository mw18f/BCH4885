#!/usr/bin/env python3
#https://github.com/mw18f/BCH4885.git
import sys
import math

##import and read a file 

def readpdb(pdbfilename):
  pdbfile= open(pdbfilename,'r')
  lines = pdbfile.readlines()
  pdbfile.close()
  return(lines)
  


#extract x,y,z coordinates and atom
def findRMSD(atomlist1,atomlist2):
  squsum = 0
  n=len(atomlist1)
  for line in atomlist1:
    vx = float(line[30:38])
    vy = float(line[38:46])
    vz = float(line[46:54])
  
    for line in atomlist2:
      wx = float(line[30:38])
      #print(wx)
      wy = float(line[38:46])
      #print(y2)
      wz = float(line[46:54])
      squ = (vx-wx)*(vx-wx) + (vy-wy)*(vy-wy) + (vz-wz)*(vz-wz)
      squsum+=squ
  
  RMSD = math.sqrt(squsum/n)
  return(RMSD)

if __name__=="__main__":
  pdbfilename = sys.argv[1]
  pdbfilename_rm = sys.argv[2]
  atomlist1 = readpdb(pdbfilename)
  atomlist2 = readpdb(pdbfilename_rm)

RMSD = findRMSD(atomlist1,atomlist2)
print(RMSD)