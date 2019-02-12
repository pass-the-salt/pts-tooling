#! /usr/bin/env python3

# Goal of the script:
# 1. take the HotCRP JSON export (+ attachments)
# 2. extract all talks details 
# 3. generate for each talk a unique file with talk informations. The generated file is based on a markdown model.

import sys
import os
import shutil
import json

MODELSDIR='models'
MODELLIST='talkslist-page-model.md'
MODELTALK='talk-page-model.md'
INDIR='input'
INJSON='hotcrp-data.json'
OUTDIR='output'
OUTPAGES='pages'
OUTTALKS='talks'
OUTIMGS=os.path.join('img', 'speakers')

if not os.path.isfile(os.path.join(INDIR, INJSON)):
    print("Could not find {}".format(os.path.join(INDIR, INJSON)))
    sys.exit(1)

# read the export file from HotCRP into a string var
with open(os.path.join(INDIR, INJSON), "r") as f:
    jsonstr = f.read()

# extract JSON data from the string var
data = json.loads(jsonstr)

# test existence of output directories (if not, create them)
if not os.path.isdir(OUTDIR):
    os.mkdir(OUTDIR)
if not os.path.isdir(os.path.join(OUTDIR, OUTPAGES, OUTTALKS)):
    os.makedirs(os.path.join(OUTDIR, OUTPAGES, OUTTALKS))
if not os.path.isdir(os.path.join(OUTDIR, OUTIMGS)):
    os.makedirs(os.path.join(OUTDIR, OUTIMGS))

# the schedule
with open(os.path.join(MODELSDIR, MODELLIST), 'r') as talkslistmodel :
    scheduledata = talkslistmodel.read()

schedule_table = ""
talkid = 0

# parse all JSON talks details: one loop round per talk
for talk_details in data:
    talkid = talkid + 1

    # Read and inject the MarkDown model file into a string
    with open(os.path.join(MODELSDIR, MODELTALK), 'r') as model :
        filedata = model.read()

    # retrieve speakers informations 
    speakers = ""
    for i,author in enumerate(talk_details['authors']):
        if i > 0:
            speakers += ", "
        speakers += "{} {}".format(author['first'], author['last'])
        if author['affiliation'] != 'None':
            speakers += " ({})".format(author['affiliation'])

    # if a bio has been provided by the authors, use it
    try:
        bio = talk_details['options']['bio'].replace('\r','')
    except KeyError:
        bio = ""

    # if an image has been provided by the authors, use it
    try:
        fn = talk_details['options']['picture-upload']['filename']
        file_name_extension = os.path.splitext(fn)[1].lower()
        potential_image_file = 'hotcrp-paper{}-picture-upload{}'.format(talk_details['pid'], file_name_extension)
        print('> ' + potential_image_file)
        if os.path.exists(os.path.join(INDIR, potential_image_file)):
            image = '![speaker](/img/speakers/{})'.format(potential_image_file)
            print('  > ' + image)
            shutil.copyfile(os.path.join(INDIR, potential_image_file), os.path.join(OUTDIR, OUTIMGS, potential_image_file))
        else:
            image = ""
    except KeyError:
        image = ""

    talk_details['abstract'] = talk_details['abstract'].replace('\r','')
    summary = talk_details['abstract'][:97]
    summary = summary.replace('\n', '; ')
    summary += "…"

    # replace place holders in the model file by the values found in talk details
    filedata = filedata.replace('###TALKID###', str(talk_details['pid']))
    filedata = filedata.replace('###TITLE###', talk_details['title'].replace(':',', '))
    filedata = filedata.replace('###SUMMARY###', summary)
    filedata = filedata.replace('###CONTENT###', talk_details['abstract'])
    filedata = filedata.replace('###SPEAKERS###', "**{}**".format(speakers))
    filedata = filedata.replace('###IMAGE###', image)
    filedata = filedata.replace('###BIO###', bio)

    # fill the schedule talk line in the talks table
    schedule_table += "| {} | [{}](/{}/{}) | {} |\n".format(talkid, talk_details['title'], OUTTALKS, talk_details['pid'], speakers)

    # Write the markdown model file (with all the talk details) into a unique file (one file per talk).
    # Filename: pid of the talk as generated by HotCRP
    with open(os.path.join(OUTDIR, OUTPAGES, OUTTALKS, "{}.md".format(talk_details['pid'])), 'w+') as outputfile:
        outputfile.write(filedata)

scheduledata = scheduledata.replace('###CONTENT###', schedule_table)
with open(os.path.join(OUTDIR, 'schedule.md'), 'w+') as outputschedule:
      outputschedule.write(scheduledata)

print("Finished conversion successfully!")
