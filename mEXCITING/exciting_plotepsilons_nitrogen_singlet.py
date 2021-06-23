#!/usr/bin/python

import matplotlib
matplotlib.use('Agg') # see http://matplotlib.org/faq/usage_faq.html#what-is-a-backend


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from lxml import etree
import os
import sys

#-------------------------------------------------------------------------------

#def shell_value(variable,vlist,default):
    #v = default
    #e = False
    #for i in range(len(vlist)):
        #if ( vlist[i] == variable ): v = os.environ[variable] ; e = True ; break
    #return v, e
    
#-------------------------------------------------------------------------------

#current = os.environ['PWD']
#ev_list = os.environ.keys()
#rundir = shell_value('EXCITINGRUNDIR',ev_list,current)[0]
#rlabel = shell_value('RLABEL',ev_list,"rundir-")[0]
#showpyplot = shell_value('SHOWPYPLOT',ev_list,"")[1]
#dpipng = int(shell_value('DPIPNG',ev_list,300)[0])

##-------------------------------------------------------------------------------
##Check arguments
#nfiles=len(sys.argv)-1
#if nfiles<1:
    #print "\nERROR: Nothing to plot!\n"
    #print "**Usage**:    PLOT-spectra.py EPSILON_FXC*.xml [ EPSILON_FXC*.xml [ EPSILON_FXC*.xml [...]]]\n"
    #sys.exit()
nfiles=3




#fnames=[]
#for i in range(nfiles):
    #fnames.append(sys.argv[i+1])
    #if not os.path.isfile(fnames[i]):
        #print "Error: file \"%s\" doesn't exist"%(fnames[i])
        #sys.exit()
#fnames=['EPSILON_BSEsinglet_SCRfull_OC11.OUT.xml','EPSILON_BSEsinglet_SCRfull_OC22.OUT.xml','EPSILON_BSEsinglet_SCRfull_OC33.OUT.xml']        
fnames=['EPSILON_BSE-singlet-TDA-BAR_SCR-full_OC11.OUT.xml','EPSILON_BSE-singlet-TDA-BAR_SCR-full_OC22.OUT.xml','EPSILON_BSE-singlet-TDA-BAR_SCR-full_OC33.OUT.xml']          
        
        
#-------------------------------------------------------------------------------
#Parse LOSS function data files
xdata=[]
ydata=[]
labels=[]
legend=[]
legends=[]
function=2
for i,fname in enumerate(fnames):
    xdata.append([])
    ydata.append([])
    labels.append({})
    #print "Parsing "+fname
    sfname = fname.split("/")[-1].split("_")
    if "FXCRPA" in sfname: legend="RPA "
    if "FXCALDA" in sfname: legend="ALDA "
    if "FXCLRCstatic" in sfname: legend="LRCstatic "
    if "FXCRBO" in sfname: legend="RBO "
    if "FXCLRCdyn" in sfname: legend="LRCdyn "
    if "FXCMB1" in sfname: legend="MB1 "
    #if not "NLF" in sfname: legend=legend+"(LFE) "
    if "NLF" in sfname: legend=legend+"(no-LFE) "
    #if sfname[-2][0:2]=="OC": legend=legend+"Optical(%s)"%(sfname[-2][2:])
    legends.append(legend)
    tree=etree.parse(fname)

    if "LOSS" in sfname: 
        rootelement = "loss"
        function = 1
        labels[i]["ylabel"] = tree.xpath('/%s/mapdef/function%d'%(rootelement,function))[0].attrib["name"]
    if "EPSILON" in sfname: 
        rootelement="dielectric"
        function = 2
        labels[i]["ylabel"] = "Im $\epsilon_M$"

    labels[i]["xlabel"] = tree.xpath('/%s/mapdef/variable1'%(rootelement))[0].attrib["name"]

    for elem in tree.xpath('/%s/map'%(rootelement)):
        xdata[i].append(float(elem.attrib["variable1"]))
        ydata[i].append(float(elem.attrib["function%d"%(function)]))

#-------------------------------------------------------------------------------
#Plot function/s 
colors=['r','g','b','y','c','m']
fig=plt.figure(1,figsize=(8,5.5))

params = {'font.size':15,
          'xtick.major.size': 5,
          'ytick.major.size': 5,
          'patch.linewidth': 1.5,
          'axes.linewidth': 2.,
          'axes.formatter.limits': (-4, 6),
          'lines.linewidth': 1.8,
          'lines.markeredgewidth':2.0,
          'lines.markersize':18,
          'legend.fontsize':11,
          'legend.borderaxespad':1,
          'legend.borderpad':0.5,
          'savefig.dpi':80}

plt.rcParams.update(params)

ax=fig.add_subplot(111)

legends=['EPSILON_BSE-singlet-TDA-BAR_SCR-full_OC11','EPSILON_BSE-singlet-TDA-BAR_SCR-full_OC22','EPSILON_BSE-singlet-TDA-BAR_SCR-full_OC33']
for i in range(nfiles):
    ax.plot(xdata[i],ydata[i],colors[np.mod(i,7)],label=legends[i])

ave=(np.array(ydata[0])+np.array(ydata[1])+np.array(ydata[2]))/3    
ax.plot(xdata[0],ave,'k-',lw=2,label='ave')    

    

ax.legend(loc=1,fontsize=8)
#ax.legend()

#ax.set_xlim(0.0,54.0)
ax.set_xlim(min(xdata[0]),max(xdata[0]))
#ax.set_xlim(4860,4900)
ax.set_xlabel(str.capitalize(labels[0]["xlabel"])+" [eV]")
if "EPSILON" in sfname: 
    ax.set_ylabel(r"Im $\epsilon_M$")
else:
    ax.set_ylabel(str.capitalize(labels[0]["ylabel"]).encode('string-escape'))

#plt.savefig('PLOT.ps',  orientation='portrait',format='eps')
plt.savefig('epsilons.png', orientation='portrait',format='png',dpi=300)

out = np.column_stack( (xdata[0],ave,ydata[0],ydata[1],ydata[2] ) )
np.savetxt('epsilons.dat', out, delimiter=" ")


#if (showpyplot): plt.show()
