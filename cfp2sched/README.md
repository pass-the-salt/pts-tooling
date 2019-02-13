# cfp2sched

**CURRENT STATUS / disclamer:** draft quality code, may not be used as-is in production. Published on the "release soon & often" mode, because it can be useful to other HotCRP users.

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
- copy `output` content to `<Jekyll root directory>`

Website regeneration: `$ jekyll serve`

## Style tuning

The schedule table is tagged with a class `.schedule` so you can easily apply some CSS selectively on it.
Similarly, the speakers pictures can be recognized by their `alt=speaker`.

CSS examples:

```css
img[alt=speaker] {
    width: 33%;
}
table.schedule {
    border-collapse: collapse;
}
table.schedule th, table.schedule td {
    border: 1px solid black; padding: 5px;
}
```

## Author(s)
- @cbrocas / @doegox

## License
GNU GENERAL PUBLIC LICENSE (GPL) Version 3
