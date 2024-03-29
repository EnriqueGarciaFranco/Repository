# -*- coding: utf-8 -*-"""Created on Tue Dec 31 14:55:52 2019 @author: ENRIQUE"""

import pandas as pd

import numpy as np

import subprocess

#@EnriqueGarciaFranco

#Import data and media

comments_name = '1.txt'

file_name = '1.mp4'

raw = pd.read_fwf( comments_name,  index=False,  header=None)

raw = np.array(raw)

time = raw[:, 0]

text = raw[:,1]

#Miliseconds appendix

extend = ',000'


#Obtain video time length

a = str(subprocess.check_output('ffprobe -i  "'+file_name+'" 2>&1 |findstr "Duration"',shell=True)) 

a = a.split(",")[0].split("Duration:")[1].strip()

msec = a[(len(a)-2):]

a = a[:(len(a)-3)]


#Formatting video time length

final_time = []

final_time.append(a)

final_time.append(',')

final_time.append(msec)

final_time.append('0')

final_time = ''.join(final_time)


#Storing and formatting time arrays

combined_array = []

index = len(time)

for i in range(index):
    
    #Last time step
    
    if i + 1 == index:
         
            init_raw = str(time[i])
            
            init = []
             
            init.append(init_raw)
             
            init.append(extend)
             
            init= ''.join(init)
             
            combined = []
            
            combined.append(init)
            
            combined.append(' -->  ')
            
            combined.append(final_time)
            
            combined= ''.join(combined)
        
            combined_array = np.append(combined_array, combined)
        
        
    #Previous time steps
            
    elif i + 1 <  index:
            
     init_raw = str(time[i])
     
     init = []
     
     init.append(init_raw)
     
     init.append(extend)
     
     init= ''.join(init)
     
     end_raw = str(time[i+1])
     
     end = []
     
     end.append(end_raw)
     
     end.append(extend)
     
     end= ''.join(end)
     
     combined = []
     
     combined.append(init)
     
     combined.append(' -->  ')
     
     combined.append(end)
     
     combined= ''.join(combined)
     
     combined_array = np.append(combined_array, combined)
     
     
#Saving arrays into .srt file
     
     
open_file = open("subtitles.srt","w")  
                 
for j in range(index):
    
    open_file.write(str(j + 1) + '\n')
    
    open_file.write(str(combined_array[j]) + '\n')
        
    open_file.write(str(text[j]) + '\n')
         
    open_file.write('' + '\n')
    
open_file.close() 
