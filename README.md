# csmetrics.org

> This repository hosts documentation and code for the webapp behind csmetrics.org. 

# Table of Contents

* [Quick start guide](#quickstart)

* [Instructions for making edits](#pushreq)

## <a name="quickstart"></a>CSmetrics.org quick start guide

**Defaults**: Load the page, and then press the green “Rank” button, this will rank 199 CRA member institutions (academic and industry) according to the aggregate weighted metrics (both measured and predicted) from 2007 to 2016 on 210 conferences. 

1. **Year slider**: use this to change the year range of the measured (citations, retrospective) and predicted (prospective) metrics. By default the two ranges are mutually exclusive, click the slider to unlock and adjust the two year ranges independently.

2. **Venue selection**: click each area keyword to toggle inclusion/exclusion of conferences in the corresponding area. The list of conferences on the lower left and the list of acronyms on the right will update correspondingly. You can use check boxes on the left to select or deselect individual conferences. 
A complete curated list of venue categories is at https://github.com/csmetrics/csmetrics.org/blob/master/app/data/venue_category.csv , data on CS journals are being reviewed and added. Submit a pull request if you’d like to propose edits to this. 

3. **Venue weighting** is set to the geometric mean of the citations for all papers in a conference (LINK TBD), you can change it to equal (i.e. each conference has a weight of 1.0) with the “Venue weight” dropdown box on the right. 
One can use the α slider to change the relative geometric weighting of the measured vs predicted metric. Small constant ε is used to prevent invalid values when an institution has zero publications in a venue. 

4. **Navigating the rank list** The following options are updated instantly without having to press the ‘Rank’ button: changing the list of institutions being ranked, change the entries per page and flip pages. 
The list of CRA member institutions are here https://github.com/csmetrics/csmetrics.org/blob/master/app/data/member_list.csv, an international list containing thousands of institutions are being curated. 

This is an pre-release version of the ranking site, feedback welcome. Changes are gladly reviewed and accepted via pull requests, other discussions and feature requests should be submitted as github issue https://github.com/csmetrics/csmetrics.org/issues


## <a name="pushreq"></a>Instructions for making edits

This project is written in python3 with Django web framework. 

1. Fork and clone this repository
1. Install Django and other requirements `$ pip install -r requirements.txt`
1. Run local server
  1. Setup env: `$ ./python manage.py migrate`
  2. Run the server: `$ ./run_server.sh`
  3. Access the server: http://localhost:8000
1. Make and test changes locally
1. Push changes to your fork and submit a pull request. 
