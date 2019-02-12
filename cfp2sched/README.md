# cfp2sched

Generate schedule table markdown file + individual markdown talk files from HotCRP `JSON export + attachments` feature.

## Prerequesites

HotCRP export : 
  - go to `https[:]//path/to/HotCRP/search?t=all&q=`
  - select all wanted talks 
  - download them selecting the `Paper information > JSON with attachments` 
  - export the `hotcrp-data.json` file and the optional photos (`hotcrp-paperXX-picture-upload.[jpg|png]`) **in an "input" directory below** `cfp2sched.py`.

## Run the script

`$ python3 cfp2sched.py`

## Output:
`cfp2sched.py` generates the following files in an `"output"` directory:
  - `schedule.md`: the schedule
  - `talks\pid.md`: the individual md files for each talk where pid is the unique id given by HotCRP. 
    - the URL of each talk is set to `/talks/pid`.
    - the links to photos are set to: `/img/speakers/hotcrp-paperXX-picture-upload.[jpg|png]` where `XX` is the pid of the talk. If no photo given during CFP, no photo is displayed.

## Inject results into Jekyll website
- copy `"output"\schedule.md` file to `<Jekyll root directory>`
- copy `"output"\talks` directory to `<Jekyll root directory>/pages` (create it if not already done)
- copy `"intput"\hotcrp-paperXX-picture-upload.[jpg|png]` to `<Jekyll root directory>/img/speakers/`

Website regeneration: `$ jekyll serve`

## Author(s)
- Christophe Brocas (@cbrocas)

## License
GNU GENERAL PUBLIC LICENSE (GPL) Version 3
