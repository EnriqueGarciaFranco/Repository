# @EnriqueGarciaFranco

#COPYPASTE .txt AND .mp4 FILE NAMES

text_file_name = 'chat.txt'

video_file_name = 'zoom_0.mp4'


#____________CODE STARTS HERE_____________

import datetime 

import pandas as pd

import numpy as np

import subprocess

import datetime

import os

#Importing text and processing comments

raw = pd.read_fwf( text_file_name,  index=False,  header=None)

raw = np.array(raw)

text_temp = raw[0:, :-2]


#Time processing and formatting

time = raw[:, 0]

#Meeting time

path = os.getcwd()

folder_name = os.path.basename(path)

meeting_time_raw = folder_name[11:19]

hours_star = int(meeting_time_raw[0:-6])
    
min_star = int(meeting_time_raw[len(meeting_time_raw)-5:-3])
    
sec_star = int(meeting_time_raw[(len(meeting_time_raw)-2):])

meeting_time = datetime.timedelta(hours = hours_star, minutes = min_star, seconds = sec_star)


time_sub = np.array([])

for time_counter in range(len(time)):
    
    time_selected = time[time_counter]
    
    hours_star = int(time_selected[0:-6])
    
    min_star = int(time_selected[len(time_selected)-5:-3])
    
    sec_star = int(time_selected[(len(time_selected)-2):])
    
    time_chosen = datetime.timedelta(hours = hours_star, minutes = min_star, seconds = sec_star)
    
    time_dif = time_chosen - meeting_time

#For subtitle times shorter than an hour, append zero at the begginning


    if time_dif.seconds < 3600:
                
            time_formatted = []
                    
            time_formatted.append('0')
                    
            time_formatted.append(str(time_dif))
                    
            time_formatted = ''.join(time_formatted)
            
            time_sub = np.append(time_sub, time_formatted)

        
    elif time_dif.seconds >= 3600:
            
            time_formatted(str(time_dif))
            
            time_sub = np.append(time_sub, time_formatted)


#Obtain video length 

video_length_temp = str(subprocess.check_output('ffprobe -i  "'+video_file_name+'" 2>&1 |findstr "Duration"',shell=True)) 

video_length_temp = video_length_temp.split(",")[0].split("Duration:")[1].strip()

msec_raw = video_length_temp[len(video_length_temp)-2:]

final_time = video_length_temp[0:-3]

final_time_temp = []

final_time_temp.append(final_time)

final_time_temp.append(',')

final_time_temp.append(msec_raw)

final_time_temp.append('0')

final_time = ''.join(final_time_temp)


#Storing and formatting time arrays

combined_array = []

index = len(time)

for i in range(index):
    
        #Start point

    
    if i + 1 <  index:

            
     init = []
     
     init.append(time_sub[i])
     
     init.append(',000')
     
     init= ''.join(init)
     
     end = []
     
     end.append(time_sub[i+1])

     end.append(',000')
     
     end= ''.join(end)
     
     combined = []
     
     combined.append(init)
     
     combined.append(' -->  ')
     
     combined.append(end)
     
     combined= ''.join(combined)
     
     combined_array = np.append(combined_array, combined)
        
#Last time step
    
    elif i + 1 == index:
         
     init = []
     
     init.append(time_sub[i])
     
     init.append(',000')
     
     init = ''.join(init)
     
     combined = []
     
     combined.append(init)
     
     combined.append(' -->  ')
     
     combined.append(final_time)
     
     combined= ''.join(combined)
     
     combined_array = np.append(combined_array, combined)
     
#Saving arrays into .srt file
     
     
open_file = open("subtitles.srt","w")  
                 
for j in range(index):
    
    open_file.write(str(combined_array[j]) + '\n')
        
    open_file.write(str(text_temp[j,-1]) + '\n')
         
    open_file.write('' + '\n')
    
open_file.close() 
