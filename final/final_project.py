##!/usr/bin/env/ python3

import sys
import argparse
from matplotlib import pyplot as plt
import numpy
import math
from optparse import OptionParser
from matplotlib_venn import venn2, venn2_circles
import os

###set argument, two input files -f1 and -f2  is required , other argument is optional 
def get_parser():
    parser = argparse.ArgumentParser(description="A program to compare promoter contacts in two different cell type")
    parser.add_argument('--inputfile1', '-f1',required=True, help = 'input first promoter contacts file')
    parser.add_argument('--inputfile2', '-f2',required=True, help = 'input second promoter contacts file')
    parser.add_argument('--pp_fig1', default = 'pp_fig1.png', help = 'Name of PP classfication of first cell type')
    parser.add_argument('--pp_fig2', default = 'pp_fig2.png', help = 'Name of PP classfication of second cell type')
    parser.add_argument('--dd_fig1', default = 'dd_fig1.png', help = 'Name of distance distribution of first cell type')
    parser.add_argument('--dd_fig2', default = 'dd_fig2.png', help = 'Name of distance distributuon of second cell type')
    parser.add_argument('--veen_plot', '-vp', default = 'veen_plot.png', help = 'Name of contacts overlap plot')
    parser.add_argument('--outdir',dest='outdir', default = os.getcwd(), help = 'Name of output directory')
    return parser

##make a dicrtiory of each column, each line is one interaction 
def readfile(filename):
    txt_file = open(filename,'r')
    lines = txt_file.readlines()
    txt_file.close()
    records=[]
    for line in lines:
        words = line.strip().split()
        
        d = {}
        d['bait_chr'] = words[0]
        d['bait_start'] = float(words[1])
        d['bait_end'] = float(words[2])
        d['bait_ID'] = int(words[3])
        d['bait_name'] = words[4]
        d['oe_chr'] = words[5]
        d['oe_start'] = float(words[6])
        d['oe_end'] = float(words[7])
        d['oe_ID']= int(words[8])
        d['oe_name']=words[9]
        d['score']=words[10]
        records.append(d)
        
    return records


#Classfication of interations into promoter promoter interactions and promoter nonpromoter interaction and calculate the their number. The total number #of interaction is the total line of inputfile, if other name is '.', this interaction is promoter non-promoter interaction, otherwise it is promoter## #promoter interaction. So n_pp = ncontatcs -n_poe
def fig1_pp(input_list,savename):
    p_oe = []
    ncontacts = len(input_list)
    for i in range(len(input_list)):
     if input_list[i]['oe_name'] == ".":
       p_oe.append(input_list[i]['oe_name'])
       n_poe = len(p_oe)
       n_pp = ncontacts - n_poe
       #plot the number of interaction using matplotlib
    names = ['All', 'P-promoter', 'P-nonpromoter']
    values = [ncontacts,n_poe,n_pp]
    plt.figure(figsize=(4,4))
    plt.bar(names, values,color = ['deeppink', 'gold', 'dodgerblue'])
    plt.suptitle('Number of interactions')
    plt.savefig(savename,dpi=150)
    


##calculating the genome distance between two DNA fragments of each contact.  First calculate the mean of two fragment coordinates. The absolute value #of subtract coordinate will be their genome distance. Append each genome distance into a list named dis
def distance(input_list):
  dis = []
  for i in range(len(input_list)):
    if input_list[i]['bait_chr'] == input_list[i]['oe_chr']:
      mean_bait = (input_list[i]['bait_start']-input_list[i]['bait_end'])/2
      mean_oe = (input_list[i]['oe_start']-input_list[i]['oe_end'])/2
      a = abs(mean_bait-mean_oe)
      dis.append(a)
  return dis

##plot the genome distance distribution of all interactions. Covert distance list into numpy array and using matplotlip plot the figure.     
def dis_plot(input_dis,savename):
  data = numpy.array(input_dis)    
  plt.figure(figsize = (4,4))
  bins_list = [0, 2000,4000,6000,8000,10000,12000,14000,16000]
  plt.hist(data, bins = bins_list,color = "dodgerblue")
  plt.suptitle('Distance Distribution')
  plt.xlabel("genome distance(bp)"); plt.ylabel("Number of interactions")
  plt.savefig(savename,dpi=150)



##find uniq contact id of each interaction based on bait ID and oe ID, sometimes it has duplicates, to remove duplicates, firstly, I put the smaller fragment ID in the fist part and large fragment ID in the second part. Then by using if ..not in.. to remove same ID in the list    
def contact_ID(input_list):
  cID = []
  for i in range(len(input_list)):
    if input_list[i]['bait_ID'] < input_list[i]['oe_ID']:
      contactID = (str(input_list[i]['bait_ID']) + '_' + str(input_list[i]['oe_ID']))
    else:
      contactID = (str(input_list[i]['oe_ID']) + '_' + str(input_list[i]['bait_ID']))
    if contactID not in cID:
      cID.append(contactID)
  return cID

##after get uniq ID of each contact in each file, using matplotlib_veen to draw veen digram of contacts in two different cell type
def veen_plot(cID_list1, cID_list2, savename):
  set1 = set (cID_list1)
  set2 = set (cID_list2)
  plt.figure(figsize = (3,3))
  venn2([set1,set2], set_labels = ("first","second"))
  plt.savefig(savename,dpi= 300)

## wirte output figures to HTML report 
def openHTML(f,title):
	f.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
""")
	f.write("<head>\n")
	f.write("<title>%s</title>\n" % title)
	f.write("</head>\n")
	f.write("<body>\n")


def writeHTMLImage(f,title, imgpath):
	f.write('<p style="font-size:30px">%s</p>\n' % title)
	f.write('<img src="%s" width="500" height="500" />\n' % imgpath)

def closeHTML(f):

	f.write("</body>\n")
	f.write("</html>\n")
	f.close()	




if __name__=="__main__":

  parser = get_parser()
  args = parser.parse_args()

##parse inputfile to readfile function  
  contacts_list1 = readfile(args.inputfile1)
  contacts_list2 =  readfile(args.inputfile2)
##parse output directory 
  os.chdir(args.outdir)
  
##parse input file to fig1_pp function  
  fig1_pp(contacts_list1,args.pp_fig1)
  fig1_pp(contacts_list2,args.pp_fig2)
  
##parse inputfile to distance function  
  dis1= distance(contacts_list1)
  dis2= distance(contacts_list2)

##parse distance list into dis_plot function  and calcalte distance median 
  dis_plot(dis1,args.dd_fig1)
  dis_plot(dis2,args.dd_fig2)
  

###parse inputfile1 and inputfile2 into contact_ID function
  cID_file1 = contact_ID(contacts_list1)
  cID_file2 = contact_ID(contacts_list2)   

##parse ID data to veen_plot function
  veen_plot(cID_file1,cID_file2,args.veen_plot)


### put output figure into HTML report 

  f = open('report.html','w')
  openHTML(f,"Promoter Capture HiC analysis")
  f.write("<h1>Process of Promoter Capture HiC Data Report </h1>")
  writeHTMLImage(f, "The number of interaction in %s " %args.inputfile1, args.pp_fig1)
  writeHTMLImage(f, "The number of interaction in %s" %args.inputfile2, args.pp_fig2)
  writeHTMLImage(f, "Distance distribution of contacts in %s" %args.inputfile1, args.dd_fig1)
  writeHTMLImage(f, "Distance distribution of contacts in %s" %args.inputfile2, args.dd_fig2)
  writeHTMLImage(f, "Overlap of promoter interactions in different cell", args.veen_plot)
  
  closeHTML(f)
  f.close()

