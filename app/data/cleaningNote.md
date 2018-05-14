## Institution data cleansing and name resolution 

We use [Microsoft Academic Graph](https://www.microsoft.com/en-us/research/project/microsoft-academic-graph/) for cleaning institution names and aliases. 

The result of the process described below are stored in `inst_fullname.csv` (containing names, urls and wikipedia urls), and `inst_alias.csv` (containing mappings of multiple surfaces strings to a single institution as described in item **1** below). 

### 1) Searching Aliases (using [MAG interpret api](https://docs.microsoft.com/en-us/azure/cognitive-services/academic-knowledge/interpretmethod))

e.g. (Searching name for a key)
```
aalto university --> aalto university
aalto university school of business --> aalto university
aalto university school of electrical engineering --> aalto university
aalto university school of science --> aalto university
```

#### We found *6729* keys from *6998* institution names
| type | count |
|------|------:|
| name == key (primary name) | *6646* |
| name != key (alias name) | *321* |
| unregistered name | *31* |

- Unregistered aliases (Updated 14/May/2018):
  - ['american university school of public affairs', 'university of ottawa faculty of medicine', 'dalhousie university faculty of engineering', 'international relief and development inc', 'faculty of civil engineering university of osijek', 'bren school of environmental science management', 'department of english university of dhaka', 'lally school of management technology', 'macquarie university faculty of human sciences', 'department of systems biology', 'faculty of humanities', 'booth school of business', 'nust school of civil and environmental engineering', 'school of industrial technology', 'faculty of architecture university of zagreb', 'asu school of sustainability', 'center for computational biology', 'burlington coat factory', 'university of łodź', 'center for bioinformatics and computational biology', 'e claiborne robins school of business', 'faculty of information technology university džemal bijedic of mostar', 'department of business management university of calcutta', 'jonkoping university foundation', 'suny poly college of nanoscale science and engineering', 'birmingham city university faculty of health', 'school of international affairs', 'farmer school of business', 'institute for computational engineering and sciences', 'faculty of law university of colombo', 'monash university faculty of medicine nursing and health sciences']


#### Common Error Types

1) Different key values for aliases

e.g.
```
at t --> at t
at t labs --> at t labs

auburn university --> auburn university
auburn university at montgomery --> auburn university at montgomery
```
current solution: rely on MAG result as it is.

2) Alias not registered or unrecognisable

e.g.
```
No search result: birmingham city university faculty of health
No result: dalhousie university faculty of engineering

No result: department of systems biology
No result: school of industrial technology
```
current solution: use the name as a key

### 2) Finding Fullname and URL of the institution (using [MAG raw data](https://www.openacademic.ai/oag/))

Affiliations.txt has (key, fullname, url, wikipedia_url) tuples.
```
$ cut -f3,4,6,7 Affiliations.txt > inst_fullname
```
