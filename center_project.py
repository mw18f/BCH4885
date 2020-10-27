#!/usr/bin/env python3
import sys
import math
#user's choice
choice=input("Do you want to center by mass or geometry 'M' or 'G': " )
##import and open pdb file 
pdbfilename=sys.argv[1]
f=open(pdbfilename)
##read every line in the file
lines=f.readlines()
f.close()
#make a atomlist
atomlist=[]
for line in lines:
  words=line.split()
  atomlist.append(words)
#open list
xmass=[]
M=[]
ymass=[]
zmass=[]
#extract x,y,z coordinates and atom
for line in lines:
  x=line[31:38]
  y=line[39:46]
  z=line[47:54]
  element=line[76:78].strip()
#assign mass of each atom
  if element=="C":
    mass=12.01
  elif element=="N":
    mass=14.01
  elif element=="O":
    mass=16.0
##calculate coordinate mutiply mass and put them into each list
  xm=float(x)*float(mass)
  ym=float(y)*float(mass)
  zm=float(z)*float(mass)
  xmass.append(xm)
  ymass.append(ym)
  zmass.append(zm)
##put mass of every atom into a list
  M.append(mass)
#caculate mass of center of x,y,z
ma=sum(xmass)/sum(M)
mb=sum(ymass)/sum(M)
mc=sum(zmass)/sum(M)

###extract x,y,z of every atom and put them into each list
xcoordinate=[]
ycoordinate=[]
zcoordinate=[]
for line in lines:
  x=line[31:38]
  y=line[39:46]
  z=line[47:54]
  xcoordinate.append(float(x))
  ycoordinate.append(float(y))
  zcoordinate.append(float(z))
##caculate geometric center of x,y,z
a=sum(xcoordinate)/int(len(xcoordinate))
b=sum(ycoordinate)/int(len(ycoordinate))
c=sum(zcoordinate)/int(len(zcoordinate))
##move x,y,z coordinate to center based on user's choice 
center=[]
for line in lines:
  x=line[31:38]
  y=line[39:46]
  z=line[47:54]
  #print(x)
  if choice=="M":  
    centerx=float(x)-ma
    centery=float(y)-mb
    centerz=float(z)-mc
  elif choice=="G":
    centerx=float(x)-a
    centery=float(y)-b
    centerz=float(z)-c 
##keep three decimal of float 
  centerx2="%.3f"%centerx
  centery2="%.3f"%centery
  centerz2="%.3f"%centerz
##format x,y,z to be standard pdb formate
  xcolumn='{:>9}'.format(centerx2)
  ycolumn='{:>8}'.format(centery2)
  zcolumn='{:>8}'.format(centerz2)
##build new file that centered point replace original one
  newline=line[0:30]+xcolumn+ycolumn+zcolumn+line[55:80]
  center.append(newline)
f.close()
##open a file for writing , convert line in list to string and save it 
file2=sys.argv[2]
f=open(file2,'w')
for line in center:
  s=str(line)
  f.write(s)
  f.write("\n")
f.close()
