# CS Metrics 2024 Edition

> Last updated 9 Oct 2024

A summary of the institution rank changes (across all CS areas/venues) between the 2023 and 2024 version is available [here](https://github.com/csmetrics/csmetrics.net/blob/master/docs/2024_update_summary/2024_update_report.pdf).

## Summary of main system and data changes


### 1. Paper filters for DBLP

[Current: Oct 2024]
* Rankings are generated using papers published from 2007 to 2023, appearing in 232 conferences and 92 journals from 15498 institutions.
* Filters for conferences: `['senior member',"what's hot", "invited", 'doctoral', 'demo', 'demonstration', 'keynote', 'student','speaker', 'tutorial', 'workshop', 'panel','competition', 'challenge']` (same as previous version.)
* Filters for journals: `['editor', 'special issue','state of the journal', 'in memory']`
(same as previous version.

[Previous: May 2023]
* Rankings are generated using papers published from 2007 to 2022, appearing in 231 conferences and 92 journals from 15498 institutions.
* Filters for conferences: `['senior member',"what's hot", "invited", 'doctoral', 'demo', 'demonstration', 'keynote', 'student','speaker', 'tutorial', 'workshop', 'panel','competition', 'challenge']` (same as previous version.)
* Filters for journals: `['editor', 'special issue','state of the journal', 'in memory']`
(same as previous version.)



### 2. Method for querying for citations

[Current: Oct 2024]
* We use [OpenAlex API](https://docs.openalex.org/) (2024-10-09 version) to query paper DOIs; then, we search paper titles if the DOI of a paper does not exist.
1.66% of papers did not match via DOI or title search.

[Previous: May 2023]
* We use [OpenAlex API](https://docs.openalex.org/) (2023-05-31 version) to query paper DOIs; then, we search paper titles if the DOI of a paper does not exist.
1.98% of papers did not match via DOI or title search.


### 3. Added new venues and categories

Updated venue list: [venue_list](https://github.com/csmetrics/csmetrics.net/blob/master/app/data/venue_list.csv)

New venue added:
* [ICSA](https://dblp.org/db/conf/icsa/index.html): International Conference on Software Architecture (conference)

New categories added: None
