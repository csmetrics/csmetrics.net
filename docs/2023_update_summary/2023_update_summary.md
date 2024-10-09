# CS Metrics 2023 Edition

> Last updated 31 May 2023

A summary of institution rank changes (across all CS areas/venues) between the 2022 and 2023 version is [here](https://github.com/csmetrics/csmetrics.net/blob/master/docs/2023_update_summary/2023_update_report.pdf).

## Summary of main system and data changes


### 1. Paper filters for DBLP

[Current: May 2023]
* Rankings are generated using papers published from 2007 to 2022, appearing in 231 conferences and 92 journals from 15498 institutions.
* Filters for conferences: `['senior member',"what's hot", "invited", 'doctoral', 'demo', 'demonstration', 'keynote', 'student','speaker', 'tutorial', 'workshop', 'panel','competition', 'challenge']` (same as previous version.)
* Filters for journals: `['editor', 'special issue','state of the journal', 'in memory']`
(same as previous version.)

[Previous: May 2022]
* Rankings are generated using papers published from 2007 to 2021, appearing in 229 conferences and 92 journals from 7315 institutions.
* Filters for conferences: `['senior member',"what's hot", "invited", 'doctoral', 'demo', 'demonstration', 'keynote', 'student','speaker', 'tutorial', 'workshop', 'panel','competition', 'challenge']` (same as previous version.)
* Filters for journals: `['editor', 'special issue','state of the journal', 'in memory']`
(same as previous version.


### 2. Method for querying for citations

[Current: May 2023]
* We use [OpenAlex API](https://docs.openalex.org/) (2023-05-31 version) to query paper DOIs; then, we search paper titles if the DOI of a paper does not exist.
1.98% of the papers did not match from DOI and title search.

[Previous: May 2022]
* We use MAG data dump (2021-12-06, the last MAG version) to query paper titles.
3.01% of the papers did not match from title search.


### 3. Added new venues and categories

Updated venue list: [venue_list](https://github.com/csmetrics/csmetrics.net/blob/master/app/data/venue_list.csv)

New venues added:
* [UCC](https://dblp.org/db/conf/ucc/): International Conference on Utility and Cloud Computing (conference)
* [BDCAT](https://dblp.org/db/conf/bdc/): International Conference on Big Data Computing, Applications and Technologies (conference)

New categories added: None
