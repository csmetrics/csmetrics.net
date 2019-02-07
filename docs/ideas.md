
## List of ideas for the next phase of CS metrics project 


### Backend

To generate [csmetrics.org](http://csmetrics.org/), we downloaded a full list of papers from [DBLP](https://dblp.org/search/) over the past 10 years (2007-2016) . We cleaned publication venue, citations, and institutional data for over 209 conferences and 80 journals. We used [Microsoft Academic Graph](https://www.microsoft.com/en-us/research/project/microsoft-academic-graph/) for cleaning institution names and aliases. See [data cleaning section](https://github.com/csmetrics/csmetrics.org/blob/8761f3bed6592db9a45a8fd9056327b67a7ed61c/docs/Overview.md#data-cleaning)  for detail.

For each venue, we identified [major topics it covers](https://github.com/csmetrics/csmetrics.org/blob/master/app/data/venue_category.csv). In the future, it may be possible to develop a methodology for grouping and analyzing sub-areas.

In the future, we plan to use  [Microsoft Academic Graph](https://www.microsoft.com/en-us/research/project/microsoft-academic-graph/) which contains scientific publication records, citation relationships between those publications, as well as authors, institutions, journals, conferences, and fields of study. We have a full data dump indexed in [ElasticSearch](https://www.elastic.co/) every 6 months including over 200M papers, 250M authors 1.4B citations, and 25K institutions. 

Here is the list of ideas for backend development:

**(Goal) Use Microsoft academic to refresh the venue and institution statistics for 2018**

    1. Implement a workflow to gather paper citaion counts from elastic search. 
    2. Implement a workflow to gather venue weights from elastic search. 
    3. Check results using citations up to 2017 and compare against the current data. 
    4. Plot the distribution of paper citation counts and validate the geometric mean heuristic. 

**(Goal) Use Microsoft academic to curate data**

    1. Filter the year/volume in our data range of interest (e.g. 2007-2019)
    2. Filter out workshop papers, demonstrations, tutorials, and everything else other than referred papers
    3. Re-generate venue weights with a new data update
    4. Interactively calculate a new ranking with the selected venues

**(Goal) Add new conferences and journals to the venue list**

    1. Workout a workflow to add new conferences/journals to the ranking
    2. Start by addressing [the issues list](https://github.com/csmetrics/csmetrics.org/issues)
    3. Compare the venue weight metric with other sources such as Google Scholar Metrics
    
**(Stretch goal) Better categorization of venues using field of study**

    1. Curate the hierarchy of the cagetories
    2. Systematically generate categories of venues



### Front end 

[csmetrics.org](http://csmetrics.org/) is developed by a few researchers who are not professional web developers or designers. It is informative and useful, but also has too much text at the same time.  Especially, as the number of venues, categories, and institutions increases, we maybe need to provide a better way to present the hierarchy of categories, or create a searchable venue list or institution list by their features. 

Here is the list of ideas for front-end development:

**(Goal) Better navigation for the site**
    1. Provide search function for the venues and research area
    2. Enable query-suggest for venues, institutions and research area
    3. Enable sorting venues by weights and categories

**(Goal) Better user interaction on categories**
    1. Improve the ways it shows categories as we have more fields or sub-fields
    2. Enable users to interact with categories better
    3. Enable on-the-fly curation of categories

**(Stretch goal) More information on-demand**

    1. Enable drilled down to get detail information for each institution 
       (e.g. its top 10 authors, fields of study, most published venue, etc)


### Community engagement and process 

We are keep getting [suggestions](https://github.com/csmetrics/csmetrics.org/issues) of adding new conferences/journals or creating new categories. 

(more - we cannot open the database to public but maybe provide its statistics or provide [unregisterd aliases](https://github.com/csmetrics/csmetrics.org/blob/master/app/data/cleaningNote.md#1-searching-aliases-using-mag-interpret-api) for human curation)

Here is the list of ideas for community engagement and process:

**(Goal) Platform to support open source contributors**

    1. Provide a way to submit a request form to add a new venue or a category (with supporting evidance)
    2. Support non-programmers to contribute for data curation


### etc

1. (Future) support fields other than Computer Science

