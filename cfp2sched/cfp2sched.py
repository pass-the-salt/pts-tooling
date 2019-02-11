#! /usr/bin/python
# Goal of the script: 
# 1. take the HotCRP JSON export (+ attachments)
# 2. extract all talks details 
# 3. generate for each talk a unique file with talk informations. The generated file is based on a markdown model.

import json
import string
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

# read the export file from HotCRP into a string var
inputfile = open(sys.argv[1], "r")
jsonstr = inputfile.read()
inputfile.close()

# extract JSON data from the string var
data = json.loads(jsonstr)

# test existence of talks output directory (if not, create it)
if not os.path.isdir('talks'):
    os.mkdir('talks')  

# the schedule
with open('talkslist-page-model.md', 'r') as talkslistmodel :
  scheduledata = talkslistmodel.read()
talkslistmodel.close()
schedule_table = ""
talkid = 0

# parse all JSON talks details: one loop round per talk
for talk_details in data:
    talkid = talkid + 1

    # Read and inject the MarkDown model file into a string
    with open('talk-page-model.md', 'r') as model :
      filedata = model.read()
    model.close()

    # retrieve speakers informations 
    speakers = ""
    last = len(talk_details['authors']) - 1

    for i,author in enumerate(talk_details['authors']):
        if author['affiliation'] !='None':
            speakers = speakers + author['first'].encode("utf-8") + " " + author['last'].encode("utf-8") + " (" + author['affiliation'].encode("utf-8") + ")"
        else:
            speakers = speakers + author['first'].encode("utf-8") + " " + author['last'].encode("utf-8") 
        if i == last:
            speakers = speakers + "."
        else:
            speakers = speakers + ", "        
    
    # if a bio has been provided by the authors, use it
    try:
        bio = talk_details['options']['bio']
    except:
        bio = ""

    # if an image has been provided by the authors, use it
    try:
        fn = talk_details['options']['picture-upload']['filename']
        s = fn.split(".")      
        file_name_extension = s[-1]
        
        potential_image_path = 'hotcrp-paper' + str(talk_details['pid']) + '-picture-upload.' + file_name_extension.lower()

        if os.path.exists("./" + potential_image_path):
            image = 'img/speakers/' + potential_image_path
        else:
            image = "/img/speakers/neutral.png"
    except:
        image = "/img/speakers/neutral.png"


    # replace place holders in the model file by the values found in talk details
    filedata = filedata.replace('###TALKID###', str(talk_details['pid']))
    filedata = filedata.replace('###TITLE###', talk_details['title'])
    filedata = filedata.replace('###SUMMARY###', talk_details['abstract'][:97] + "...")
    filedata = filedata.replace('###CONTENT###', talk_details['abstract'])
    filedata = filedata.replace('###SPEAKERS###', speakers)  
    filedata = filedata.replace('###IMAGE###', image)
    filedata = filedata.replace('###BIO###', bio)
    
    # fill the schedule talk line in the talks table
    schedule_table = schedule_table + "| " + str(talkid) + " | [" + talk_details['title'] + "](/talks/" + str(talk_details['pid']) + ") | " + speakers + " |\n"

    # Write the markdown model file (with all the talk details) into a unique file (one file per talk). 
    # Filename: pid of the talk as generated by HotCRP
    with open('talks/' + str(talk_details['pid']) + ".md", 'w+') as outputfile:
      outputfile.write(filedata)
    outputfile.close()

scheduledata = scheduledata.replace('###CONTENT###', schedule_table)
with open('schedule.md', 'w+') as outputschedule:
      outputschedule.write(scheduledata)
outputschedule.close()

print "Finished conversion successfully!"
