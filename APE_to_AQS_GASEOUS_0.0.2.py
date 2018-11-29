#%%
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 13:21:10 2018
Updated on Nov 15
Last Updated on Nov16

@author: bcubrich



SUMMARY
--------------------------------
This code takes audit files for gaseous data and collects the audit and 
indicated measurements, then outputs a pipe delimited text file called
 'QA_output.txt' that can be directly uploaded to AQS.

INDEX
-------------------------------
1. Functions
    -functions to get filenames and directories    

2. Retrieve Data
    -Section of the code to get a list of startion parameter 
    (State Code, County Code, Paramter Metho, Etc.) , and also to get the 
    files that the user wishes to create an AQS import file for
    
3. Create Output Dataframe
    -Take the data from the user input audit forms and convert it to a pandas
    data frame (df). This is done partly because of how I find and assign the level 
    values, but also because a pandas dataframe can quickly and easily be written 
    to a pipe ('|') delimited text file, which is use to to upload the data

4. Write to file 
    -Write the above df to a file

5. Testing
    -Not used here. Was create to check if this script was working, but 
    actually became useful for error checking data already in AQS    

6. Update AQS
    -If the above finds error in AQS then this will write and AQS update file
    that can fix some types of mistakes



"""





import pandas as pd
import numpy as np         #didn't even use numpy!!! HA!
#import seaborn as sns
from tkinter import Tk
from tkinter.filedialog import askopenfilename
#import matplotlib.pyplot as plt
import os
#import xlrd
import wx

'''---------------------------------------------------------------------------
                                1. Functions
----------------------------------------------------------------------------'''

#The following functions are just used to get filepaths
#I usually just run it once to get the path, and then leave this 
#fucntion so that I can get othe rpaths if needed
def get_dat():
    root = Tk()
    root.withdraw()
    root.focus_force()
    root.attributes("-topmost", True)      #makes the dialog appear on top
    filename = askopenfilename()      # Open single file
    root.destroy()
    return filename

#Thanks Kristy Weber 11/15/18 for giving me these functions to specify directories
def audit_path():
    app = wx.App()
     
    frame = wx.Frame(None, -1, 'win.py')
    frame.SetSize(0,0,200,50)
     
    # Create open file dialog
    openFileDialog = wx.DirDialog(frame, "Choose directory with audit data", "",
                wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
     
    openFileDialog.ShowModal()
    print(openFileDialog.GetPath())
    
    # outfile_path is the string with the path name saved as a variable
    path = openFileDialog.GetPath()#+'\\'
    openFileDialog.Destroy()
    
    del app
    return path


def get_outpath():
    #function to get output path of file
    app = wx.App()
     
    frame = wx.Frame(None, -1, 'win.py')
    frame.SetSize(0,0,200,50)
     
    # Create open file dialog
    openFileDialog = wx.DirDialog(frame, "Choose output file directory", "",
                wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
     
    openFileDialog.ShowModal()
    print(openFileDialog.GetPath())
    
    # outfile_path is the string with the path name saved as a variable
    out_path = openFileDialog.GetPath()
    openFileDialog.Destroy()
    
    del app
    
    return out_path

'''---------------------------------------------------------------------------
                            2. Retrieve Data
---------------------------------------------------------------------------'''


sites=r'U:/PLAN/BCUBRICH/Python/Parameter Reader/'\
r'PARAMETERS.xls'

sites_df=pd.read_excel(sites, converters={'SITE NAME':str,'State Code':str,
                                          'County Code':str, 'Site Code':str,
                                          'Paramter':str, 'Analyt':str, 
                                          'Method':str, 'Unit':str}) # load data
sites_df['Analyt']=sites_df['Analyt'].str.strip('()') #strip parentheses from 

#This is the original path for when I wrote the code
#directory='U:/PLAN/BCUBRICH/Python/Parameter Reader/tests'

#get the path where the data are stored
directory=audit_path()

#I copied these columns right out of a pipe delimeted text file, and just 
#pasted them here. Need to load this as a big text string here
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

#Then break it into column headers here
columns=columns_raw.split('|')

#Next, create empty df. This is very important. In order to upload the output file
#when everything is done we need to make sure there are a specific number of 
#pipes. The easiest way I can see to do that is to create a df with the right
#number of columns, then fill only those columns. When the df is written to a 
#csv we can just specify '|' as the sep, and it will put in pipes for each of
#of the empty rows.
output_df=pd.DataFrame(columns=columns)    

count=0 #just want to be able to check if we looped all the files


'''---------------------------------------------------------------------------
                         3. Create Output Dataframe
                         
This section focuses on the pandas df 'output_df'. I use this df to store up
all the info needed for an AQS upload that can be easily saved to a pipe 
delimited csv.
----------------------------------------------------------------------------'''


for filename in os.listdir(directory):     #loop through files in user's dir
    if filename.endswith(".xls") or filename.endswith(".xlsx"):
#        print(filename)     #this is useful for double checking the files are read
        
        file=filename.split('/')[-1][:-4]   #Get the filename minus the extension
        site_name=file[:2]                  #Get sitename from filename
        if site_name=='OG' : site_name='O2' #OG is an old site, it's now called O2
        if site_name=='HA' : site_name='HW' #double naming...
        
        analyt=file.split()[2]              #Find out what was being measured from filename
        #Sometime people use the following interchangeably, but we only want the NO2 instrument name
        if analyt.upper() == 'NOX' or analyt.upper() == 'NO' : analyt = 'NO2'
        
        #next line gets the info about the insturment and site from the Paramters... list
        loc_deets=sites_df[(sites_df['Site Symbol']==site_name)&\
                           (sites_df['Analyt'].str.contains\
                            (analyt.upper()))].reset_index()
        
        #fill in the parts of the df that will be the same for every entry
        output_df.loc[count,'Transaction Type']='QA'
        output_df.loc[count,'Action Indicator']='I'
        output_df.loc[count,'Assessment Type']='Annual PE'
        output_df.loc[count,'Performing Agency']='1113'
        output_df.loc[count,'State Code / Tribal Indicator']='49'
        
        #need to change the date from the format in the filename to the AQS format
        date=file.split()[1]                               #get date from filename
        date_split=date.split('-')                         #split on'-'
        date_fmt=date_split[2]+date_split[0]+date_split[1] #rearrange
        
        
        if len(loc_deets)>=1:           #this if prevents some errors when there wasn't a match
            if len(loc_deets)==2: loc_deets=loc_deets[loc_deets['POC']=='1']
            #This section saves all the information about the site to the out_put 
            #df in the AQS format.
            output_df.loc[count,'County Code / Tribal Code']=loc_deets.loc[0,'County Code']
            output_df.loc[count,'Site Number']=loc_deets.loc[0,'Site Code']
            output_df.loc[count,'Parameter Code']=int(loc_deets.loc[0,'Parameter'])
            output_df.loc[count,'POC']=loc_deets.loc[0,'POC']
            output_df.loc[count,'Assessment Date']=date_fmt
            output_df.loc[count,'Assessment Number']=1
            output_df.loc[count,'Monitor Method Code']=loc_deets.loc[0,'Method']
            output_df.loc[count,'Reported Unit']=loc_deets.loc[0,'Unit']
        
            
            #for NO2, NOx
            skiprows=31
            n_rows=9
            usecols=[1,8,9]
            
            #need some if's here because the different excel spreadsheets
            #have data in different places. These if's just specify where the
            #data is saved in the excel file.
            if analyt == 'O3':
                skiprows=24
                n_rows=5
                usecols=[1,3,5]
            if analyt == 'SO2':
                skiprows=21
                n_rows=4
                usecols=[1,3,4]
            if analyt == 'CO':
                skiprows=21
                n_rows=4
                usecols=[2,4,5]
            
            #Read in the audit workbook
            wb=pd.read_excel((directory+'/'+filename), skiprows =skiprows, 
                             n_rows=n_rows, usecols=usecols, 
                         names=['Audit Level', 'Audit', 'Indicated'])
            
            #There are two forms of ozone workbooks, so we need some if's
            #here to make sure that we get the right one. This works by 
            #looking to see if there are any levels entries in the the first wb
            if analyt == 'O3' and wb['Audit Level'].isna().sum()>=7:
#                print('HERE!!!!') #just to help debug where the old )3 forms were used
                skiprows=25
                n_rows=5
                usecols=[2,4,6]
                wb=pd.read_excel((directory+'/'+filename), skiprows =skiprows, 
                             n_rows=n_rows, usecols=usecols, 
                         names=['Audit Level', 'Audit', 'Indicated'])
            
            no_match=0
            #need this if because you get some errors if the wb df is empty.
            #There are several reasons this might happen, so if you do get not
            #matches it requires some debugging. The most likely cause is a 
            #non standardized form.
            if wb.empty==True:
                no_match+=1
#                print('Non match '+str(int(no_match))+' = ' +filename)
            else:
                #get rid of rows where there was no Level or Indicated value reported
                wb=wb.dropna(subset = ['Indicated', 'Audit Level'])
                wb=wb.set_index('Audit Level')
                
                
                for level in wb.index:
                    level = int(level)
#                    print (level)    #for debug
                    #these next lines are where the magic happens. I find the
                    #levels contained in the audit file, then concat a string
                    #with the column name in the output_df that corresponds 
                    #to the level. By writing there, it makes sure that the
                    #correct number of pipes will be included in the AQS file.
                    col_name='Level '+str(level)+' Assessment Concentration'
                    output_df.loc[count,col_name]=wb.loc[level, 'Audit']
                    col_name='Level '+str(level)+' Monitor Concentration'
                    output_df.loc[count,col_name]=wb.loc[level, 'Indicated']
            
        else:
            print ('No site location matched')
        count+=1
        continue
    else:
        continue




'''----------------------------------------------------------------------------
                             4.  Write to file
---------------------------------------------------------------------------'''



out_path = get_outpath() #get user selected output path


output_df=output_df.set_index('Transaction Type') #need to get rid of index
output_df.to_csv(out_path+'\QA_output.txt', sep='|')    #write to pipe file


'''---------
The following whole bit is used to add a '#' to the first line of the file. 
Seems like a lot of code just to add a hashtag to the file, but I like having 
the header info right in the file, in case someone only sees the text file.
------'''
appendText='#'
text_file=open(out_path+'\QA_output.txt','r')
text=text_file.read()
text_file.close()
text_file=open(out_path+'\QA_output.txt','w')
text_file.seek(0,0)
text_file.write(appendText+text)
text_file.close()

#%%

'''--------------------------------------------------------------------------
                                 5. Testing
                                  
-This whole part of the script is  used to check if previously uploaded data
on AQS is accurate. It requires a file called 'verify', which is a pipe-
delimited output file from AQS of the Audit data over a given period.
The error checking is not exactly straight forward. 
---------------------------------------------------------------------------'''
testing=False      #set to true if you want to do some testing
if testing==True:
    output_file=open('U:/PLAN/BCUBRICH/Python/Parameter Reader/QA_output.txt','r')
    out=output_file.read()
    out_lines=out.split('\n')
    verify_file=open('U:/PLAN/BCUBRICH/Python/Parameter Reader/verify.txt','r')
    vers=verify_file.read()
    vers_lines=vers.split('\n')
    print(len(out_lines))
    match=0
    count_err=0
    count_err2=0
    conv_cols=r'Level 1 Monitor Concentration|Level 1 '\
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
        
    conv_cols=conv_cols.split('|')
    conv_dict=dict()
    missed=[]
    
    def unq(seq):
       # Not order preserving    
       Set = set(seq)
       return list(Set)
    
    for item in conv_cols:
        conv_dict[item]=float
    
    
    for line1 in out_lines:
        for line2 in vers_lines:
            if line1==line2:
                match+=1
            else:
                
                if line1[:38]==line2[:38]:
                    
                    df_check_temp=pd.DataFrame([line1.split('|'), line2.split('|')], columns=columns)
                    df_check_temp[conv_cols]=df_check_temp[conv_cols].apply(pd.to_numeric)
                    
                    if count_err==0:
                        df_check=df_check_temp.copy()
                    else:
                        df_check=df_check.append(df_check_temp)
                    
                    count_err+=1
    
    for line1 in out_lines:
        if line1 in vers_lines:
            something=1
        else:
            if line1[:38] in vers_lines:
                something=1
            else:
                print(line1)
            
                    
    before=len(df_check)
    df_check=df_check.drop_duplicates(keep=False)
    after=len(df_check)
    match=match+(before-after)/2
    match+=5
    print(match)
    

'''----------------------------------------------------------------------------
                                     6. Update AQS
                                    
You can create an update file from the found errors in the above
testing section here. These can be directly uploaded to 
----------------------------------------------------------------------------'''
update=False #change this if you want to run this.
if update==True:
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
