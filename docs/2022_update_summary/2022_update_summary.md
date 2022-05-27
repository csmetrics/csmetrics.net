# CS Metrics 2022 Edition

> Last updated 27 May 2022

A summary of institution rank changes (across all CS areas/venues) between the 2021 and 2022 version is [here](https://github.com/csmetrics/csmetrics.org/blob/master/docs/2022_update_summary/2022_update_report.pdf).

## Summary of main system and data changes


### 1. Paper filters for DBLP

[Current: May 2022]
* Rankings are generated using papers published from 2007 to 2021, appearing in 229 conferences and 92 journals from 7315 institutions.
* Filters for conferences: `['senior member',"what's hot", "invited", 'doctoral', 'demo', 'demonstration', 'keynote', 'student','speaker', 'tutorial', 'workshop', 'panel','competition', 'challenge']` (same as previous version.)
* Filters for journals: `['editor', 'special issue','state of the journal', 'in memory']`
(same as previous version.

[Previous: June 2021]
* Rankings are generated using papers published from 2007 to 2020, appearing in 229 conferences and 90 journals from 6793 institutions.
* Filters for conferences: `['senior member',"what's hot", "invited", 'doctoral', 'demo', 'demonstration', 'keynote', 'student','speaker', 'tutorial', 'workshop', 'panel','competition', 'challenge']` (same as previous version.)
* Filters for journals: `['editor', 'special issue','state of the journal', 'in memory']`
(same as previous version.)


### 2. Method for querying for citations

[Current: May 2022]
* We use MAG data dump (2021-12-06, the last MAG version) to query paper titles.
3.01% of the papers did not match from title search.

[Previous: June 2021]
* We use MAG data dump (2021-02-15 version) to query paper titles.
2.87% of the papers did not match from title search.
MAG data now support multiple affiliations per author.

### 3. Added new venues and categories

Updated venue list: [venue_list](https://github.com/csmetrics/csmetrics.org/blob/master/app/data/venue_list.csv)

New venues added:
* [TMI](https://dblp.org/db/journals/tmi/): IEEE Transactions on Medical Imaging (journal)
* [PACMHCI](https://dblp.uni-trier.de/db/journals/pacmhci/): Proceedings of the ACM on Human-Computer Interaction (journal)

New categories added: None
