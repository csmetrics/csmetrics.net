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

#### We found *6231* keys from *6245* institution names (Updated 11/July/2019)
| type | count |
|------|------:|
| name == key (primary name) | *6231* |
| name != key (alias name) | *13* |
| unregistered name | *1* |

- Unregistered aliases :
  - ['german cancer research center']


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
No result: department of systems biology
No result: school of industrial technology
```
current solution: use the name as a key

### 2) Finding Fullname and URL of the institution (using [MAG raw data](https://www.openacademic.ai/oag/))

Affiliations.txt has (key, fullname, grid, url, wikipedia_url) tuples.
```
$ cut -f3,4,5,6,7 Affiliations.txt > inst_fullname
```
