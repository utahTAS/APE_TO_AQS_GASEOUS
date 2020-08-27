# APE_to_AQS_GASEOUS

This python code takes audit files for gaseous data and collects the audit and indicated measurements, then outputs a pipe delimited text file called 'QA_output.txt' that can be directly uploaded to AQS.
This reduces the chances of human Typo mistakes, and improves the speed of uploading such files. This tool also has some sections for looking for mistakes in previously uploaded AQS data and fixing them.
During testing, several mistakes were identified and corrected, and a new set of 3 audits was uploaded to AQS in under a minute.


## Getting Started

To get this program working you just need to save the python file to a computer that has a python IDE and a connection to the DAQ shared U: drive.

## Prerequisites

I recommend anaconda/spyder as a python IDE, but choose whatever you want. This was built and works on python 3.7.

also need these modules in pyhton

python -comes with anaconda

pandas -comes with anaconda

numpy  -comes with anaconda

tkinter -comes with anaconda

os      -comes with anaconda

wx      -needs to be instaled, with the anaconda promt 'conda install -c anaconda wxpython', else  'pip install wxpython'

## Usage example

1. Place the audit files you want to upload in your folder of choice. ie.g. U://PLAN/AMC/BCUBRICH/AUDITS/TODAYS_DATE 
2. Run this script
3. Select the folder where the files are with the dialog box , so in this case U://PLAN/AMC/BCUBRICH/AUDITS/TODAYS_DATE 
4. Code will run, then ask you to select output folder, I usually use the saem folder, i.e. U://PLAN/AMC/BCUBRICH/AUDITS/TODAYS_DATE 
5. Double check that the file 'QA_output.txt' has the same number of entries as files, and the the data are correct
     -This can also be done in the spyder IDE by looking at the dataframe 'output_df', which is easier to read that 'QA_output.txt'
6. Log in to the ENSC website and upload the file 'QA_output.txt'
7. Log in to AQS, navigate to Batch, and check that the upload occured succefully
8. As a final QC, you can query the uploaded data under AQS>Maintain>QA Assessments>Annual Performance Evaluation

## Installing

1. Save the python '.py' file to your computer
2. Run it in python IDE

## Release History

0.0.1
   -First Stable Release
0.0.2
   -Fixed a small bug in reading in O3 files
"standard_form"
   _Uses as stardardized form to ensure consistent data extraction for all parameters.

## Built With

python and freinds

## Authors

Bart Cubrich


## Meta

Bart Cubrich
bcubrich@utah.gov


## License

This work has been identified as being free of known restrictions under copyright law, including all related and neighboring rights.
You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission. See Other Information below.
The work may not be free of known copyright restrictions in all jurisdictions.
Persons may have other rights in or related to the work, such as patent or trademark rights, and others may have rights in how the work is used, such as publicity or privacy rights.
In some jurisdictions moral rights of the author may persist beyond the term of copyright. These rights may include the right to be identified as the author and the right to object to derogatory treatments.
Unless expressly stated otherwise, the person who identified the work makes no warranties about the work, and disclaims liability for all uses of the work, to the fullest extent permitted by applicable law.
When using or citing the work, you should not imply endorsement by the author or the person who identified the work.

## Acknowledgments

Thanks Kristy Weber for the wxpython directory search bit at the begining of this code.
