# How to Update csmetrics.org


## 0. Backup Old Data

Backup the previous data as follows:
- `app/data/venue_list.csv` -> `app/data/venue_list_2023.csv`
- `app/data/venue_weight.csv` -> `app/data/venue_weight_2023.csv`
- `data/filtered_papers` -> `data/filtered_papers_2023`
- `data/scores` -> `data/scores_2023`


## 1. Crawl New Data

Run the script — [/data/get_and_clean_DBLP_papers.ipynb](https://github.com/csmetrics/csmetrics.org/blob/master/data/get_and_clean_DBLP_papers.ipynb)

- **Files to Update**:
  - `/app/data/venue_list.csv` — Update categories and add new venues
  - `venues_with_different_dblp_keys.csv` — A list of venues using different keys
  - `venues_with_different_dblp_baseurls.csv` — A list of venues using different base URLs
  - `journals_to_use_alternative_scraping_method.csv` — Journals using an alternative scraping method

- **Change the Year Ranges (also applies to the files above)**:
  ```python
  # change year range
  for year in range(2007, 2021):    
  ```


## 2. Retrieve Citation and Affiliation Data

Run the script — [/data/get_paper_data_from_OpenAlex.ipynb](https://github.com/csmetrics/csmetrics.net/blob/master/data/get_paper_data_from_OpenAlex.ipynb)

The `get_paper_data_from_OpenAlex.py` script is also available for the same function.

Note: It’s recommended to copy the existing filtered paper data and retrieve only the data for the new years. After that, instead of using `get_information_for_venue_papers`, run `try_again_venue_papers` to retry fetching OpenAlex IDs for papers that previously could not be found.

  ```python
  def task(venues):
    for venue, venuetype in venues:
        # get_information_for_venue_papers(venue, venuetype)
        try_again_venue_papers(venue, venuetype)
    return None 
  ```


## 3. Calculate Venue Weight

Run script — [/data/score_papers.ipynb](https://github.com/csmetrics/csmetrics.net/blob/master/data/score_papers.ipynb)
to calculate weight of the affiliations

Then run [/data/score_venues.ipynb](https://github.com/csmetrics/csmetrics.net/blob/master/data/score_venues.ipynb)
