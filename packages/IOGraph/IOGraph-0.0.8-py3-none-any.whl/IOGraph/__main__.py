#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def iograph():
    """Generate Graphs for IOZone."""
    global _iograph
    if _iograph: return _iograph

import pkg_resources
version = pkg_resources.require("IOGraph")[0].version
import os
import codecs
import os.path
import sys
import csv
import ast
import re
import json
import math
import yaml
import xlrd
import argparse
from argparse import RawTextHelpFormatter
import pkg_resources
import appdirs
import platform
import subprocess
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from numpy.random import seed, rand
from pprint import pprint
from datetime import date
from base64 import b64encode


__version__="0.0.1"

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

version=__version__

##ArgumentParser
IOGraphMoTD='IOGraph\nVersion: '
IOGraphMoTD+=str(__version__)
IOGraphMoTD+='\nGenerate Graphs from IOZone Data'
parser = argparse.ArgumentParser(description=IOGraphMoTD, formatter_class=RawTextHelpFormatter
                   )
parser.add_argument('--version', action='version', version=version
                   )
parser.add_argument("-d","--dryrun",
                    help='Generate Graph from existing XLS file',nargs='+'
                   )
parser.add_argument("-v","--verbose",
                    help="increase output verbosity.",
                    action="store_true"
                   )
parser.add_argument("-a","--average", type=int,
                    help="run IOZone X times and average the results."
                   )
parser.add_argument("-c","--compare",
                    help="path to another IOzone generated XLS to compare results against."
                   )
parser.add_argument("-s","--settings",
                    help="the parameters that you want to run IOzone with."
                   )
parser.add_argument("-E","--executable",
                    help="path to the IOZone Executable."
                   )
parser.add_argument("-m","--mute",
                    help="mute all output.",
                    action="store_true"
                   )
parser.add_argument("-o","--outputfile",
                    help="specify the name of the output file, defaults to output."
                   )
parser.add_argument("-f","--filename",
                    help="specify the path and filename that IOzone Runs against."
                   )
parser.add_argument("-i","--testtype",
                    help='Test to run:\n\t0=write/rewrite, 1=read/re-read, 2=random-read/write\n\t3=Read-backwards, 4=Re-write-record, 5=stride-read, 6=fwrite/re-fwrite\n\t7=fread/Re-fread, 8=random_mix, 9=pwrite/Re-pwrite, 10=pread/Re-pread\n\t11=pwritev/Re-pwritev, 12=preadv/Re-preadv'
                   )
parser.add_argument("-I","--directio",
                    help='Use DIRECT IO if possible for all file operations. Tells the filesystem that all operations to the file are to bypass the buffer cache and go directly to disk. (not available on all platforms)'
                   )
parser.add_argument("-g","--maxfilesize",
                    help="Set maximum file size (in Kbytes) for auto mode. One may also specify -g #k (size in Kbytes) or -g #m (size in Mbytes) or -g #g (size in Gbytes). See -n for minimum file size."
                   )
parser.add_argument("-n","--minfilesize",
                    help="Override the minimum filesize used for test to Bypass system buffer."
                   )                  
parser.add_argument("-q","--maxrecordsize",
                    help="Set maximum record size (in Kbytes) for auto mode. One may also specify -q #k (size in Kbytes) or -q #m (size in Mbytes) or -q #g (size in Gbytes). See -y for minimum record size."
                   )
parser.add_argument("-r","--recordsize",
                    help="Used to specify the record size, in Kbytes, to test. One may also specify -r #k (size in Kbytes) or -r #m (size in Mbytes) or -r #g (size in Gbytes)."
                   )
parser.add_argument("-y","--minrecordsize",
                    help="Set minimum record size (in Kbytes) for auto mode. One may also specify -y #k (size in Kbytes) or -y #m (size in Mbytes) or -y #g (size in Gbytes). See -q for maximum record size."
                   )
parser.add_argument("-F","--filesize",
                    help="Used to specify the size, in Kbytes, of the file to test. One may also specify -s #k (size in Kbytes) or -s #m (size in Mbytes) or -s #g (size in Gbytes).."
                   )
parser.add_argument("-U","--unmount",
                    help="Mount point to unmount and remount between tests. Iozone will unmount and remount this mount point before beginning each test. This guarantees that the buffer cache does not contain any of the file under test."
                   )                                    
parser.add_argument("-u","--cpu",
                    help="Include CPU results in Reports.",
                    action="store_true"
                   )
parser.add_argument("-z","--smallrecords",
                    help="Used in conjunction with -a to test all possible record sizes. Normally Iozone omits testing of small record sizes for very large files when used in full automatic mode. This option forces Iozone to include the small record sizes in the automatic tests also.",
                    action="store_true"
                   )
parser.add_argument("-e","--flush",
                    help="Include flush (fsync,fflush) in the timing calculations.",
                    action="store_true"
                   )
parser.add_argument("-M","--uname",
                    help="Iozone will call uname() and will put the string in the output file.",
                    action="store_true"
                   )

## Configuration File
def get_config():
  cfg_dir = appdirs.user_config_dir('IOGraph')
  cfg_file = os.path.join(cfg_dir, 'conf.yml')
  if not os.path.isfile(cfg_file):
      isDir = os.path.isdir(cfg_dir) 
      if not isDir:
          os.mkdir(cfg_dir)
      create_user_config(cfg_file)
  with open(cfg_file) as f:
      config = yaml.load(f.read(), Loader=yaml.FullLoader)
      return config

def create_user_config(cfg_file):
    source = pkg_resources.resource_stream(__name__, 'conf.yml.dist')
    with open(cfg_file, 'wb') as dest:
        dest.writelines(source)

cfg = get_config()



## Detect Which System we are Running on
System=os.name
Platform=platform.system()
PlatformRelease=platform.release()

args = parser.parse_args()
if args.dryrun:
    dryRun=args.dryrun
    
if not args.average:
    averageRun=1   
else:
    averageRun=args.average

if not args.outputfile:
    outputFile="output"
else:
    outputFile=args.outputfile

if not args.settings:
    IOSettings="Rab"   
else:
    IOSettings=args.settings


if not args.executable:
    executable="/opt/ooce/bin/iozone"   
    WindowsEXE='C:\Program Files (x86)\Benchmarks\Iozone3_483\iozone.exe'
    OmniOSEXE="/opt/ooce/bin/iozone"
    TrueNASEXE="/usr/local/bin/iozone"
    CentOSEXE="/usr/bin/iozone"
    UbuntuEXE="/usr/bin/iozone"
else:
    executable=args.executable

if  args.verbose:
    print("Verbose: ",args.verbose)
    print("Dry Run: ",args.dryrun)
    print("Averaging Runs: ",averageRun)
    print("Comparing Against: ",args.compare)
    print("IOZone Settings: ",IOSettings)
    print("This System is : ",System)
    print("It's Platform is: ",Platform)
    print("It's Release is: ",PlatformRelease)
    print("IOzone is Running across the filename: ",args.filename)


def current_path():
    cwd=os.getcwd()
    return cwd

if not args.filename:
    cwd=current_path()
    cwd+="IOZoneTestFile"
    if  args.verbose:
        print(cwd)
else:
    cwd=args.filename
    if  args.verbose:
        print(cwd)

## Begin of Annot
def annot(xcrd,ycrd, zcrd, txt, yancr='bottom'):
    strng=dict(showarrow=False, x=xcrd, y=ycrd, z=zcrd, text=txt, yanchor=yancr, font=dict(color=cfg['plot']['annotation']['COLOR'],size=cfg['plot']['annotation']['SIZE']))
    return strng
## End of Annot

## Begin runIO Function
def runIO():
    ## Run the Command to Grab the Data -- Add Flags Later for Different Reports
    loc=[]
    for x in range(0,averageRun):
        if not args.dryrun:
            if not args.verbose:
                command="nohup "
                command+=executable
                command+=" -"
                command+=IOSettings
                command+=" "
                command+=outputFile
                command+="-"
                command+=str(x+1)
                command+='.xls '
                if args.testtype:
                    command+="-i "
                    command+=args.testtype
                    command+=" "
                if args.cpu:
                    command+=" -+u "
                if args.maxfilesize:
                    command+="-g "
                    command+=args.maxfilesize
                    command+=" "
                if args.minfilesize:
                    command+="-n "
                    command+=args.minfilesize
                    command+=" "
                if args.smallrecords:
                    command+=" -z "
                if cwd:
                    command+="-f "
                    command+=cwd
                    command+=" "
                command+='> IO-output.log  2>&1'
                print(command)
                iozonertndata = subprocess.Popen(command, shell=True)
                iozonertndata.wait()
                ## Define the location of the output file
                locfile=""
                locfile+=outputFile
                locfile+="-"
                locfile+=str(x+1)
                locfile+=".xls"
                loc.append(locfile)
                if not args.mute:
                    print()
                    print("Run:",x+1," Filename: ",locfile)
            else:
                if not args.mute:
                    print()
                    print("This is the ",x+1," Run")
                command=""
                command+=executable
                command+=" -"
                command+=IOSettings
                command+=" "
                command+=outputFile
                command+="-"
                command+=str(x+1)
                command+='.xls'
                if args.testtype:
                    command+="-i "
                    command+=args.testtype
                    command+=" "
                if args.maxfilesize:
                    command+="-g "
                    command+=args.maxfilesize
                    command+=" "
                if args.minfilesize:
                    command+="-n "
                    command+=args.minfilesize
                    command+=" "
                if args.cpu:
                    command+=" -+u "
                if args.smallrecords:
                    command+=" -z "
                if cwd:
                    command+=" -f "
                    command+=cwd
                print(command)
                iozonertndata = subprocess.Popen(command, shell=True)
                iozonertndata.wait()
                ## Define the location of the output file
                locfile=""
                locfile+=outputFile
                locfile+="-"
                locfile+=str(x+1)
                locfile+=".xls"
                loc.append(locfile)
                if not args.mute:
                    print()
                    print("Run:",x+1," Filename: ",loc)
        else:
            for arg in args.dryrun:
                loc.append(arg)
    return loc    
## End runIO Function

## Begin of Trace
def Trace(clr,data):
    X = []
    Y = []
    Z = []
    for datum in data:
        X.append(float(datum[0]))
        Y.append(float(datum[1]))
        Z.append(float(datum[2]))
    if 'plot' in cfg:
        if 'trace' in cfg['plot']:
            if 'COLOR' in cfg['plot']['trace']:
                traceColor=cfg['plot']['trace']['COLOR']
            else:
                traceColor=Z
    if 'plot' in cfg:
        if 'trace' in cfg['plot']:
            if 'COLOR' in cfg['plot']['line']:
                lineColor=cfg['plot']['line']['COLOR']
            else:
                lineColor=Z
    ##Trace each Scatter 3d Trace
    trace=go.Scatter3d(
                       x=X,
                       y=Y,
                       z=Z, 
                       mode="lines+markers", 
                       marker = dict(
                           size = cfg['plot']['trace']['SIZE'],
                           color = traceColor,
                           #fill="toself",
                           showscale=True,
                           coloraxis="coloraxis",
                           colorscale = cfg['plot']['trace']['COLORSCALE']
                           ),
                       line=dict(
                           color=lineColor,
                           colorscale = cfg['plot']['line']['COLORSCALE'],
                           coloraxis="coloraxis",
                           width=cfg['plot']['line']['width']
                           )
                       )
    return trace   
## End of Trace

## Begin reportTrace Function
def reportTrace(reports):
    reportMatrix = []
    XData=[]
    YData=[]
    ZData=[]
    Data=[]
    dataCount = 0
    for reportData in reports[1:]:
        ## If the First Row start with Zero, then it is the Y Axis
        if dataCount == 0:
            YData=reportData[1:]
        ## The Remaing Rows are the X Axis and the Z Axis
        else:
            ## The First column is the X Axis Data
            XData.append(reportData[:1][0])
            ## remove any Empty Z values Not record as Zero
            ZDatarow=[float(i) if i.strip() else 0. for i in reportData[1:].tolist()]
            ## Change the Values to Strings for easier processing
            ZDatarow=[str(ZDatarow) for ZDatarow in ZDatarow]
            ## Save the Z Axis Data
            ZData.append(ZDatarow)
        ## Increment the Datacount so that we can get the Y data
        dataCount += 1	
    ## Create the Full Report Matrix
    for xcount, xvalue in enumerate(XData):
        for ycount, yvalue in enumerate(YData):
            reportMatrix.append([xvalue, YData[ycount], ZData[xcount][ycount]])
    Variables=[]
    Traces=LineUp(reportMatrix)    
    Variables.append(Traces)
    Variables.append(XData)
    Variables.append(YData)
    Variables.append(ZData)
    return Variables
## End of reportTrace

## Begin LineUp
def LineUp(reportMatrix):
    data=[]
    prevRow=[]
    Traces=[]
    trace=[]
    for row in reportMatrix:
        ## Setup The Trace Array 
        if not prevRow:
            pass
        elif prevRow != row[0]:
            ## New X detected, save the old one
            Traces.append(trace)            
        ## New Row Detected, Start new Trace to save to the Trace Array
        if prevRow != row[0]:
            trace=[]
            trace.append(row)
        else:
            ## Existing Row Detected, Keep in same loop
            trace.append(row)
        prevRow=row[0]
    Traces.append(trace)
    return Traces        
### End of LineUp Function

## Begin of ReportData Function
def ReportData(file):
    ## Open the Excel Spreadsheet
    if not args.mute:
        print("Working on File: ", file)
    workbook=xlrd.open_workbook(file, encoding_override='cp1252')

    ## Use the first Index (because IOZone doesn't give us any others that I know of)
    sheet = workbook.sheet_by_index(0)

    ## Each Report Header Contains the Word Report
    reportString="Report"  
    reportCount = 0
    rowsinreportCount = 0
    reports = []
    report = []
    PlotTitles=[]

    ## Seperate out each Report
    for i in range(3,sheet.nrows):
       npArray = np.array(sheet.row_values(i)).astype(str)
       if reportString in npArray[0]:
           PlotTitles.append(npArray[0])
           if not len(report) == 0:
               reports.append(report)
           report = []
           report.append(npArray[0])
           reportCount += 1
           rowsinreportCount = 0          
       else:
          report.append(npArray)
          rowsinreportCount += 1
    reports.append(report)

    ## Mute if unwanted
    if not args.mute:
        print()
        print("There are: ",reportCount," Reports")
        print()
    Variables=[]
    Variables.append(reports)
    Variables.append(reportCount)
    Variables.append(PlotTitles)
    return Variables
## End Report Data Function

## Begin Figures Function
def figures(reports,reportCount,PlotTitles):
    Reports = []
    ## Loop Through all reports and turn them into Traces
    rcount=0
    zMax=0
    zMin=0
    rData=[]
    rDataset=[]
    for report in reports:
        rcount+=1
        rData=reportTrace(report)
        rDataset.append(rData)
        LineTraces=[]

        ## For Each Line Trace, pass it to the Graphing function Trace
        for line in rData[0]:
            LineTraces.append(Trace(cfg['plot']['color'],line))
            for lineD in line:
                if  float(lineD[2]) > zMax:
                    zMax=float(lineD[2])
        Reports.append(LineTraces)
    Variables=[]
    zRange=[]
    zRange.append(zMin)
    zRange.append(zMax)
    Variables.append(reportCount)
    Variables.append(Reports)
    Variables.append(rData)
    Variables.append(PlotTitles)
    Variables.append(rDataset)
    Variables.append(zRange)
    return Variables
## End figures Function

## Begin graphReports Function
def graphReports(reportCount,Reports,rData,PlotTitles,Range):
    if not args.mute:
        print("Generating graph")

    Annot=[]
    ### Setup up the Canvas
    ## Set up the Camera
    camera = dict(
        up=dict(
                x=cfg['plot']['camera']['up']['X'],
                y=cfg['plot']['camera']['up']['Y'],
                z=cfg['plot']['camera']['up']['Z']
                ),
        center=dict(
                x=cfg['plot']['camera']['center']['X'],
                y=cfg['plot']['camera']['center']['Y'],
                z=cfg['plot']['camera']['center']['Z']),
        eye=dict(
                x=cfg['plot']['camera']['eye']['X'],
                y=cfg['plot']['camera']['eye']['Y'],
                z=cfg['plot']['camera']['eye']['Z']
                )
    )
    
    ## Specify the Scene type for each Trace
    spectale=[]
    scenestuff=[{'type': 'scatter3d'}]
    for i in range(reportCount):
        spectale.append(scenestuff)

    ## Configure to Figure to use the Layout Defined above
    if not args.verbose:
        fig = make_subplots( rows=reportCount, 
                        subplot_titles=(PlotTitles),
                        start_cell=cfg['plot']['startcell'],
                        horizontal_spacing = cfg['plot']['spacing']['horizontal'],
                        vertical_spacing = cfg['plot']['spacing']['vertical'],
                        shared_xaxes=cfg['plot']['shared_xaxes'],
                        shared_yaxes=cfg['plot']['shared_yaxes'],
                        specs=spectale
                        )
    else:     
        fig = make_subplots( rows=reportCount, 
                        subplot_titles=(PlotTitles),
                        start_cell=cfg['plot']['startcell'],
                        horizontal_spacing = cfg['plot']['spacing']['horizontal'],
                        vertical_spacing = cfg['plot']['spacing']['vertical'],
                        shared_xaxes=cfg['plot']['shared_xaxes'],
                        shared_yaxes=cfg['plot']['shared_xaxes'],
                        print_grid=True,
                        specs=spectale
                        )
    
    ##Setup the Layout
    if args.verbose:
        pprint(PlotTitles) 
    fig.update_layout(
                     margin=dict(
                                 l=cfg['plot']['margin']['l'],
                                 r=cfg['plot']['margin']['r'],
                                 t=cfg['plot']['margin']['t'],
                                 b=cfg['plot']['margin']['b'],
                                 pad=cfg['plot']['margin']['pad']
                                ),
                     height = cfg['plot']['height']*reportCount,
                     title = {
                         'text': cfg['plot']['title']['text'],
                         'y': cfg['plot']['title']['X'],
                         'x': cfg['plot']['title']['Y'],
                         'xanchor': cfg['plot']['title']['XANCHOR'],
                         'yanchor': cfg['plot']['title']['YANCHOR']},
                     showlegend=cfg['plot']['legend']['show'],
                     #legend=dict(traceorder="reversed"),
                     paper_bgcolor = cfg['plot']['paper']['COLOR']
                     )

    ##For each report, for each line in it's set of Traces, add the figure to the plot
    rscount=0
    for subReports in Reports:   
       rscount += 1
       for lineTraces in subReports:
            fig.add_trace(lineTraces,row=rscount, col=1)
        
    ## Setup The Scenes
    fig.update_scenes(            camera = camera,
                                  xaxis=dict(
                                             title=cfg['plot']['sector']['Title']['X'],
                                             type=cfg['plot']['lines']['type']['X'],
                                             zeroline=cfg['plot']['zeroline']['X'],
                                             autorange=cfg['plot']['lines']['autorange']['X'],
                                             zerolinecolor=cfg['plot']['zeroline']['COLOR']['X'],
                                             zerolinewidth=cfg['plot']['zeroline']['width']['X'],
                                             tickmode = 'array',
                                             tickvals = rData[1],
                                             ticktext = rData[1],
                                             showline=cfg['plot']['lines']['show']['X'],
                                             linewidth=cfg['plot']['lines']['width']['X'],
                                             linecolor=cfg['plot']['lines']['COLOR']['X'],
                                             ticks = cfg['plot']['tick']['ticks']['X'],
                                             showgrid = cfg['plot']['tick']['showgrid']['X'],
                                             tickprefix = cfg['plot']['tick']['prefix']['X'],
                                             tickcolor = cfg['plot']['tick']['COLOR']['X'],    
                                             tickwidth = cfg['plot']['tick']['width']['X'],
                                             ticklen = cfg['plot']['tick']['length']['X'],
                                             tickangle = cfg['plot']['tick']['angle']['X'],
                                             titlefont_color=cfg['plot']['sector']['COLOR']['X'],
                                             backgroundcolor=cfg['plot']['background']['COLOR']['X'],
                                             color=cfg['plot']['axis']['COLOR']['X'],
                                             gridcolor=cfg['plot']['grid']['COLOR']['X']
                                  ),
                                  yaxis=dict(
                                             title=cfg['plot']['sector']['Title']['Y'],
                                             type=cfg['plot']['lines']['type']['Y'],
                                             autorange=cfg['plot']['lines']['autorange']['Y'],
                                             zeroline=cfg['plot']['zeroline']['Y'],
                                             zerolinecolor=cfg['plot']['zeroline']['COLOR']['Y'],
                                             zerolinewidth=cfg['plot']['zeroline']['width']['Y'],
                                             tickmode = 'array',
                                             tickvals = rData[2],
                                             ticktext = rData[2],
                                             showline=cfg['plot']['lines']['show']['Y'],
                                             linewidth=cfg['plot']['lines']['width']['Y'],
                                             linecolor=cfg['plot']['lines']['COLOR']['Y'],
                                             ticks=cfg['plot']['tick']['ticks']['Y'],
                                             showgrid=cfg['plot']['tick']['showgrid']['Y'],
                                             tickprefix = cfg['plot']['tick']['prefix']['Y'],
                                             tickwidth = cfg['plot']['tick']['length']['Y'],
                                             tickcolor = cfg['plot']['tick']['COLOR']['Y'],                                              
                                             ticklen = cfg['plot']['tick']['width']['Y'],                                             
                                             tickangle = cfg['plot']['tick']['angle']['Y'],                                             
                                             titlefont_color=cfg['plot']['sector']['COLOR']['Y'],
                                             backgroundcolor=cfg['plot']['background']['COLOR']['Y'],
                                             color=cfg['plot']['axis']['COLOR']['Y'],
                                             gridcolor=cfg['plot']['grid']['COLOR']['Y']
                                   ),
                                  zaxis=dict(
                                             nticks=cfg['plot']['grid']['nticks']['Z'],
                                             tickformat="s3",
                                             autorange=cfg['plot']['lines']['autorange']['Z'],
                                             rangemode=cfg['plot']['lines']['rangemode']['Z'],
                                             showline=cfg['plot']['lines']['show']['Z'],
                                             linewidth=cfg['plot']['lines']['width']['Z'],
                                             linecolor=cfg['plot']['lines']['COLOR']['Z'],
                                             ticks=cfg['plot']['tick']['ticks']['Z'],
                                             showgrid=cfg['plot']['tick']['showgrid']['Z'],
                                             tickprefix = cfg['plot']['tick']['prefix']['Z'],
                                             tickcolor = cfg['plot']['tick']['COLOR']['Z'],    
                                             zeroline=cfg['plot']['zeroline']['Z'],
                                             zerolinecolor=cfg['plot']['zeroline']['COLOR']['Z'],
                                             zerolinewidth=cfg['plot']['zeroline']['width']['Z'],
                                             title=cfg['plot']['sector']['Title']['Z'],
                                             tickangle = cfg['plot']['tick']['angle']['Z'],                                             
                                             tickwidth = cfg['plot']['tick']['width']['Z'],
                                             ticklen = cfg['plot']['tick']['length']['Z'],
                                             titlefont_color=cfg['plot']['sector']['COLOR']['Z'],
                                             backgroundcolor=cfg['plot']['background']['COLOR']['Z'],
                                             color=cfg['plot']['axis']['COLOR']['Z'],
                                             gridcolor=cfg['plot']['grid']['COLOR']['Z'],
                                             range=[Range[0], Range[1]]
                                  ),
                     )
    return fig
## End graphReports Function

## Begin compare Function
def compare(figureData,operation):
    ## Check if we need to Generate Figure Data to Compare against and Grab that data, assuming only one file
    comparativeData=[]   
    ## Grab the Report Data From the File
    if not args.mute:
        print("Pulling Comparative Data")

    compData=ReportData(args.compare)
    
  
    ## Save the Report data to ComparativeData and Generate it's Figures for later Graphing
    comparativeData.append(figures(compData[0],compData[1],compData[2]))  
    
    zipReports=zip(comparativeData[0][4],figureData[0][4])    


    ## use the rDataset from Figures function for both the current and the comparativedata
    zMax=0
    zMin=0
    allDifs=[]
    for zcompData,zRData  in zipReports:
        zcData=zcompData[3]
        zrData=zRData[3]
        xData=zRData[1]
        yData=zRData[2]
        zip_object = zip(zrData,zcData)
        differences=[]
        ## Zip up each row  and prepare to subtract it
        for compData,figData  in zip_object:                
            zobject=zip(compData,figData)
            difference=[]
            for c,f  in zobject:
                if operation == "subtract":
                    difference.append(float(c)-float(f))
                    if  (float(c)-float(f) > zMax):
                        zMax=(float(c)-float(f))
                    if  (float(c)-float(f)) < zMin:
                        zMin=(float(c)-float(f))
            differences.append(difference)
        allDifs.append(differences)
    zRange=[]
    zRange.append(zMin)
    zRange.append(zMax)
    allrX=[]
    Reports=[]

    for dif in allDifs:
        rX=[] 
        rDataset=[]
        rData=[]
        for xc, xv in enumerate(xData):   
            for yc, yv in enumerate(yData): 
                rX.append([ xv,  yData[yc], str(dif[xc][yc])])
        rData.append(LineUp(rX))
        rData.append(xData)
        rData.append(yData)
        rDataset.append(rData)
        LineTraces=[]
        ## For Each Line Trace, pass it to the Graphing function Trace
        for line in rData[0]:
            LineTraces.append(Trace(cfg['plot']['color'],line))
        Reports.append(LineTraces)
    Variables=[]
    Variables.append(figureData[0][0])
    Variables.append(Reports)
    Variables.append(rData)
    Variables.append(figureData[0][3])
    Variables.append(rDataset)
    Variables.append(zRange)
    return Variables
## End compare Function


## Begin Main
def main():
    ## Disable the Plotly Logo
    config = {'displaylogo': False} 
    
    ## Generate or Gather XLS files
    loc=runIO()

    ## Generate a Figure for each File
    ffigureData=[]
    graphData=[]
    for file in loc:
        repData=ReportData(file)      
        ffigureData.append(figures(repData[0],repData[1],repData[2]))
    
    operation=[]
       ## Check if we are doing an Average Calculation
    if not averageRun:
        print(averageRun)
        operation="average"
        print("We need to Average the Results")
        ## If this is a Dry run we may have an issue, skipping for now
        print(len(ffigureData))
        #figureData.append(compare(figureData,operation))
    
    
    ## Compare the Output with another
    if args.compare: 
        print()
        operation="subtract"
        crepData=ReportData(args.compare)
        ffigureData.append(figures(crepData[0],crepData[1],crepData[2]))
        ffigureData.append(compare(ffigureData,operation))
        
        
    ## Graph Each figure
    for figcount, figs in  enumerate(ffigureData):
        graphs=graphReports(figs[0],figs[1],figs[2],figs[3],figs[5])
        graphData.append(graphs)
        
    ## Write out the Visualization for each XLS file
    for graphcount, graph in  enumerate(graphData):
        htmloutputFile=""
        htmloutputFile=""
        htmloutputFile+=outputFile
        htmloutputFile+="-"
        htmloutputFile+=str(graphcount+1)
        htmloutputFile+=".html"      
        graph.write_html(htmloutputFile, config=config)           
## End Main

main()
