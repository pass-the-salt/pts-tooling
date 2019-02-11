# cfp2sched

Generate schedule table markdown file + individual markdown talk files from HotCRP "JSON export + attachments" feature.

##Prerequesites:##

HotCRP export : 
  - go to `https[:]//path/to/HotCRP/search?t=all&q=`
  - select all wanted talks 
  - download them selecting the "Paper information > JSON with attachments" 
  - export the `hotcrp-data.json` file and the optional photos (`hotcrp-paperXX-picture-upload.jpg or png`) **in the same directory that** `cfp2sched.py`.

## Run the script

`$ python cfp2sched.py hotcrp-data.json`

## Output:
  - the schedule will be written to the file: `schedule.md`
  - the individual md files for each talk will be written to: `talks/pid` (pid is unique id given by HotCRP, the URL of each talk is set to `/talks/pid`)
  - links to photos are set to: `/img/speakers/hotcrp-paperXX-picture-upload.xxx` where `XX` is the pid of the talk. If no photo given during CFP, the photo used is `neutral.png`.

## Authors
- Christophe Brocas (@cbrocas)

## License
GNU GENERAL PUBLIC LICENSE (GPL) Version 3
