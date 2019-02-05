
## List of ideas for the next phase of CS metrics project 


### Backend

To generate [csmetrics.org](http://csmetrics.org/), we downloaded a full list of papers from [DBLP](https://dblp.org/search/) over the past 10 years (2007-2016) and . We cleaned publication venue, citations, and institutional data for over 209 conferences and 80 journals. We used [Microsoft Academic Graph](https://www.microsoft.com/en-us/research/project/microsoft-academic-graph/) for cleaning institution names and aliases. See [data cleaning section](https://github.com/csmetrics/csmetrics.org/blob/8761f3bed6592db9a45a8fd9056327b67a7ed61c/docs/Overview.md#data-cleaning)  for detail.

For each venue, we identified [major topics it covers](https://github.com/csmetrics/csmetrics.org/blob/master/app/data/venue_category.csv). In the future, it may be possible to develop a methodology for grouping and analyzing sub-areas.

In the future, we plan to use  [Microsoft Academic Graph](https://www.microsoft.com/en-us/research/project/microsoft-academic-graph/) which contains scientific publication records, citation relationships between those publications, as well as authors, institutions, journals, conferences, and fields of study. We have a full data dump indexed in [ElasticSearch](https://www.elastic.co/) every 6 months including over 200M papers, 250M authors 1.4B citations, and 25K institutions. 

Here is the list of ideas for backend development:
1. Automation process to get data from ElasticSearch to calculate venue weights
    1. Filter the year/volume in our data range of interest (e.g. 2007-2019)
    2. Filter out workshop papers, demonstrations, tutorials, and everything else other than referred papers
    3. Re-generate venue weights whenever we have a new data update
2. Better categorization of venues using field of study
    1. Curate the hierarchy of the cagetories
    2. Systematically generate categories of venues


### Front end 

[csmetrics.org](http://csmetrics.org/) is developed by a few researchers who are not professional web developers or designers. It is informative and useful, but also has too much text at the same time.  Especially, as the number of venues, categories, and institutions increases, we maybe need to provide a better way to present the hierarchy of categories, or create a searchable venue list or institution list by their features. 

(detail information for institutions)

Here is the list of ideas for front-end development:
1. Better look and feel of csmetrics.org
    1. Search or sort the venues by their categories or weights
    2. Better way to show categories as we have more fields or sub-fields
2. More information for institutions
    1. Provide detail information for each institution (e.g. its top 10 authors, fields of study, most published venue, etc)


### Community engagement and process 

We are keep getting [suggestions](https://github.com/csmetrics/csmetrics.org/issues) of adding new conferences/journals or creating new categories. 

(more - we cannot open the database to public but maybe provide its statistics or provide [unregisterd aliases](https://github.com/csmetrics/csmetrics.org/blob/master/app/data/cleaningNote.md#1-searching-aliases-using-mag-interpret-api) for human curation)

Here is the list of ideas for community engagement and process:
1. Supporting open source contributors
    1. Provide a form for evidence for adding a new venue or a category
    2. ???


### etc

1. (Future) support fields other than Computer Science

