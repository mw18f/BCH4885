#!/usr/bin/env python3

f=open("2FA9noend.pdb",'r')

lines=f.readlines()

atomlist=[]
for  line  in  lines:
  words=line.split()
  atomlist.append(words)
#print(atomlist)
f.close()

f=open("alist.txt",'w')
for line in atomlist:
  s=str(line)
  f.write(s)
  f.write("\n")
f.close()


print("Done!")