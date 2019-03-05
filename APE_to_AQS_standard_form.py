#%%
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 13:21:10 2018

@author: bcubrich
"""

import pandas as pd
import numpy as np
import seaborn as sns
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import matplotlib.pyplot as plt
import os
#import xlrd
#import wx

#The following function is just used to get filepaths
#I usually just run it once to get the path, and then leave this 
#fucntion so that I can get othe rpaths if needed
def get_dat():
    root = Tk()
    root.withdraw()
    root.focus_force()
    root.attributes("-topmost", True)      #makes the dialog appear on top
    filename = askdirectory()      # Open single file
    
    return filename


#def onButton2(event):
# 
#app = wx.App()
# 
#frame = wx.Frame(None, -1, 'win.py')
#frame.SetDimensions(0,0,200,50)
# 
## Create open file dialog
#openFileDialog = wx.DirDialog(frame, "Choose folder to save output to", "",
#            wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
# 
#openFileDialog.ShowModal()
#print(openFileDialog.GetPath())
#
## outfile_path is the string with the path name saved as a variable
#outfile_path = openFileDialog.GetPath()+'\\'
#openFileDialog.Destroy()
#
#del app

sites=r'U:/PLAN/BCUBRICH/Python/Parameter Reader/'\
r'PARAMETERS.xls'

sites_df=pd.read_excel(sites, converters={'SITE NAME':str,'State Code':str,
                                          'County Code':str, 'Site Code':str,
                                          'Paramter':str, 'Analyt':str, 
                                          'Method':str, 'Unit':str}) # load data
sites_df['Analyt']=sites_df['Analyt'].str.strip('()') #strip parentheses from 

directory=get_dat()

columns_raw=r'Transaction Type|Action Indicator|Assessment Type|Performing '\
        r'Agency|State Code / Tribal Indicator|County Code / Tribal Code|Site '\
        r'Number|Parameter Code|POC|Assessment Date|Assessment Number|Monitor '\
        r'Method Code|Reported Unit|Level 1 Monitor Concentration|Level 1 '\
        r'Assessment Concentration|Level 2 Monitor Concentration|Level 2 '\
        r'Assessment Concentration|Level 3 Monitor Concentration|Level 3 '\
        r'Assessment Concentration|Level 4 Monitor Concentration|Level 4 '\
        r'Assessment Concentration|Level 5 Monitor Concentration|Level 5 '\
        r'Assessment Concentration|Level 6 Monitor Concentration|Level 6 '\
        r'Assessment Concentration|Level 7 Monitor Concentration|Level 7 '\
        r'Assessment Concentration|Level 8 Monitor Concentration|Level 8 '\
        r'Assessment Concentration|Level 9 Monitor Concentration|Level 9 '\
        r'Assessment Concentration|Level 10 Monitor Concentration|Level '\
        r'10 Assessment Concentration'
        
        
        
        
columns=columns_raw.split('|')

output_df=pd.DataFrame(columns=columns)
count=0
for filename in os.listdir(directory):
    if filename.endswith(".xls") or filename.endswith(".xlsx"):
#        print(filename)
        file=filename.split('/')[-1][:-4]
        site_name=file[:2]
        if site_name=='OG' : site_name='O2'
        analyt=file.split()[2]
        
        loc_deets=sites_df[(sites_df['Site Symbol']==site_name)&\
                           (sites_df['Analyt'].str.contains(analyt.upper()))].reset_index()
        
        output_df.loc[count,'Transaction Type']='QA'
        output_df.loc[count,'Action Indicator']='I'
        output_df.loc[count,'Assessment Type']='Annual PE'
        output_df.loc[count,'Performing Agency']='1113'
        output_df.loc[count,'State Code / Tribal Indicator']='49'
        
        date=file.split()[1]
        date_split=date.split('-')
        date_fmt=date_split[2]+date_split[0]+date_split[1]
        
        if len(loc_deets)>=1:
            output_df.loc[count,'County Code / Tribal Code']=loc_deets.loc[0,'County Code']
            output_df.loc[count,'Site Number']=loc_deets.loc[0,'Site Code']
            output_df.loc[count,'Parameter Code']=int(loc_deets.loc[0,'Parameter'])
            output_df.loc[count,'POC']=loc_deets.loc[0,'POC']
            output_df.loc[count,'Assessment Date']=date_fmt
            output_df.loc[count,'Assessment Number']=1
#            output_df.loc[count,'Monitor']=1
            output_df.loc[count,'Monitor Method Code']=loc_deets.loc[0,'Method']
            output_df.loc[count,'Reported Unit']=loc_deets.loc[0,'Unit']
        
            
            #for NO2, NOx
            skiprows=10
            n_rows=10
            usecols=[0,2,4]
            
            #need some if's here because the different excel spreadsheets
            #have data in different places
#            if analyt == 'O3':
#                skiprows=24
#                n_rows=5
#                usecols=[1,3,5]
#            if analyt == 'SO2':
#                skiprows=21
#                n_rows=4
#                usecols=[1,3,4]
#            if analyt == 'CO':
#                skiprows=21
#                n_rows=4
#                usecols=[2,4,5]
#            
            #Read in the audit workbook
            wb=pd.read_excel((directory+'/'+filename), skiprows =skiprows, 
                             n_rows=n_rows, usecols=usecols, 
                         names=['Audit Level', 'Audit', 'Indicated'])
            
            #There are two forms of ozone workbooks, so we need some if's
            #here to make sure that we get the right one. This works by 
            #looking to see if there are any levels entries in the the first wb
#            if analyt == 'O3' and wb['Audit Level'].isna().sum()>=7:
##                print('HERE!!!!')
#                skiprows=24
#                n_rows=5
#                usecols=[2,4,6]
#                wb=pd.read_excel((directory+'/'+filename), skiprows =skiprows, 
#                             n_rows=n_rows, usecols=usecols, 
#                         names=['Audit Level', 'Audit', 'Indicated'])
                
            no_match=0
            if wb.empty==True:
                no_match+=1
#                print('Non match '+str(int(no_match))+' = ' +filename)
            else:
                wb=wb.dropna(subset = ['Indicated', 'Audit Level'])
                wb=wb.set_index('Audit Level')
                
                
                for level in wb.index:
                    level = int(level)
#                    print (level)
                    col_name='Level '+str(level)+' Assessment Concentration'
                    output_df.loc[count,col_name]=wb.loc[level, 'Audit']
                    col_name='Level '+str(level)+' Monitor Concentration'
                    output_df.loc[count,col_name]=wb.loc[level, 'Indicated']
            
                
        count+=1
        continue
    else:
        continue


column_div=r'Level 1 Monitor Concentration|Level 1 '\
        r'Assessment Concentration|Level 2 Monitor Concentration|Level 2 '\
        r'Assessment Concentration|Level 3 Monitor Concentration|Level 3 '\
        r'Assessment Concentration|Level 4 Monitor Concentration|Level 4 '\
        r'Assessment Concentration|Level 5 Monitor Concentration|Level 5 '\
        r'Assessment Concentration|Level 6 Monitor Concentration|Level 6 '\
        r'Assessment Concentration|Level 7 Monitor Concentration|Level 7 '\
        r'Assessment Concentration|Level 8 Monitor Concentration|Level 8 '\
        r'Assessment Concentration|Level 9 Monitor Concentration|Level 9 '\
        r'Assessment Concentration|Level 10 Monitor Concentration|Level '\
        r'10 Assessment Concentration'.split('|')

iter_df=pd.DataFrame(columns=columns)
for line in output_df.iterrows():
    line=line[-1]
    if line['Reported Unit']=='008' and any(i>60 for i in line[column_div].values):
        for col in column_div:
            line[col]=line[col]/1000
    iter_df=iter_df.append(line)
output_df=iter_df.copy()



output_df=output_df.set_index('Transaction Type')#.drop('Index', axis=0)
output_df.to_csv(directory+'\QA_output.txt', sep='|')    #write to pipe file

'''This whole bit is used to add a '#' to the first line of the file'''
appendText='#'
text_file=open(directory+'\QA_output.txt','r')
text=text_file.read()
text_file.close()
text_file=open(directory+'\QA_output.txt','w')
text_file.seek(0,0)
text_file.write(appendText+text)
text_file.close()

#
#'''--------------------------------------------------------------------------
#                                  Testing
#                                  
#-This whole part of the script is  used to check if previously uploaded data
#on AQS is accurate. It requires a file called 'verify', which is a pipe-
#delimited output file from AQS of the Audit data over a given period.
#The error checking is not exactly straight forward. 
#---------------------------------------------------------------------------'''
#
#
#output_file=open('U:/PLAN/BCUBRICH/Python/Parameter Reader/QA_output.txt','r')
#out=output_file.read()
#out_lines=out.split('\n')
#verify_file=open('U:/PLAN/BCUBRICH/Python/Parameter Reader/verify.txt','r')
#vers=verify_file.read()
#vers_lines=vers.split('\n')
#print(len(out_lines))
#match=0
#count_err=0
#count_err2=0
#conv_cols=r'Level 1 Monitor Concentration|Level 1 '\
#        r'Assessment Concentration|Level 2 Monitor Concentration|Level 2 '\
#        r'Assessment Concentration|Level 3 Monitor Concentration|Level 3 '\
#        r'Assessment Concentration|Level 4 Monitor Concentration|Level 4 '\
#        r'Assessment Concentration|Level 5 Monitor Concentration|Level 5 '\
#        r'Assessment Concentration|Level 6 Monitor Concentration|Level 6 '\
#        r'Assessment Concentration|Level 7 Monitor Concentration|Level 7 '\
#        r'Assessment Concentration|Level 8 Monitor Concentration|Level 8 '\
#        r'Assessment Concentration|Level 9 Monitor Concentration|Level 9 '\
#        r'Assessment Concentration|Level 10 Monitor Concentration|Level '\
#        r'10 Assessment Concentration'
#    
#conv_cols=conv_cols.split('|')
#conv_dict=dict()
#missed=[]
#
#def unq(seq):
#   # Not order preserving    
#   Set = set(seq)
#   return list(Set)
#
#for item in conv_cols:
#    conv_dict[item]=float
#
#
#for line1 in out_lines:
#    for line2 in vers_lines:
#        if line1==line2:
#            match+=1
#        else:
#            
#            if line1[:38]==line2[:38]:
#                
#                df_check_temp=pd.DataFrame([line1.split('|'), line2.split('|')], columns=columns)
#                df_check_temp[conv_cols]=df_check_temp[conv_cols].apply(pd.to_numeric)
#                
#                if count_err==0:
#                    df_check=df_check_temp.copy()
#                else:
#                    df_check=df_check.append(df_check_temp)
#                
#                count_err+=1
#
#for line1 in out_lines:
#    if line1 in vers_lines:
#        something=1
#    else:
#        if line1[:38] in vers_lines:
#            something=1
#        else:
#            print(line1)
#        
#                
#before=len(df_check)
#df_check=df_check.drop_duplicates(keep=False)
#after=len(df_check)
#match=match+(before-after)/2
#match+=5
#print(match)


'''----------------------------------------------------------------------------
                                    Update
                                    
You can create an update file from the found errors in the above
testing section here. These can be directly uploaded to 
----------------------------------------------------------------------------'''

df_update=df_check.loc[0,:].set_index('Transaction Type')
df_update['Action Indicator']='U'
df_update.to_csv('U:/PLAN/BCUBRICH/Python/Parameter Reader/QA_update.txt', sep='|')   

'''This whole bit is used to add a '#' to the first line of the file'''
appendText='#'
text_file=open('U:/PLAN/BCUBRICH/Python/Parameter Reader/QA_update.txt','r')
text=text_file.read()
text_file.close()
text_file=open('U:/PLAN/BCUBRICH/Python/Parameter Reader/QA_update.txt','w')
text_file.seek(0,0)
text_file.write(appendText+text)
text_file.close()
