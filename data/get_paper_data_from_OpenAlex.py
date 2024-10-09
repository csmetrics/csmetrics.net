# Import necessary libraries
import os, json, csv, time, requests
from datetime import datetime
from multiprocessing import Pool

# Import filtering functions for papers
from paper_filtering import (
    filter_by_header,
    filter_by_page_number_keep_missing,
    filter_by_page_number_remove_missing,
    filter_by_header_and_page_number_keep_missing,
    filter_by_header_and_page_number_remove_missing,
    filter_journals,
    apply_filter_to_papers
)

# Set the number of threads for multiprocessing
threads = 8

# Define the range of years to process (2007 to 2023)
yearrange = range(2007, 2024)

# Filepath to the venue list (CSV file containing venue names and their categories)
venue_category_filename = os.path.join(os.pardir, "app", "data", "venue_list.csv")

# Define filename patterns for raw DBLP data and filtered papers
dblp_raw_filename = lambda name, year: os.path.join("DBLP_raw_data", f"{name}_{year}_raw_dblp_papers.json")
filtered_papers_filename = lambda name, year: os.path.join("filtered_papers", f"{name}_{year}_filtered_papers.json")

# OpenAlex API URL for fetching paper information
OPENALEX_WORK_API = "https://api.openalex.org/works"


# Function to fetch paper information from OpenAlex by DOI
def get_openalex_paper_info(paper):
    query_url = f'{OPENALEX_WORK_API}/{paper["doi"]}?select=id,doi,display_name,publication_year,authorships,cited_by_count'
    response = requests.get(query_url)

    if response.status_code == 200:
        data = response.json()
        institutions = {}
        for authorship in data["authorships"]:
            num_insts = len(authorship["institutions"])
            for inst in authorship["institutions"]:
                inst_name = inst.get("display_name", "")
                institutions[inst_name] = institutions.get(inst_name, 0) + 1 / num_insts

        return [{
            "PaperId": data["id"],
            "PaperTitle": data["display_name"],
            "Year": data["publication_year"],
            "CitationCount": data["cited_by_count"],
            "EstimatedCitation": data["cited_by_count"],
            "Affiliations": institutions,
            "Authors": [a["author"]["display_name"] for a in data["authorships"]]
        }]
    else:
        return get_openalex_paper_info_title_search(paper)


# Fallback function to search for a paper by title if DOI search fails
def get_openalex_paper_info_title_search(paper):
    query_url = f'{OPENALEX_WORK_API}?filter=title.search:"{paper["title"]}"&select=id,doi,display_name,publication_year,authorships,cited_by_count'
    response = requests.get(query_url)
    if response.status_code == 200:
        result = response.json()
        matched = []
        for data in result["results"]:
            institutions = {}
            for authorship in data["authorships"]:
                num_insts = len(authorship["institutions"])
                for inst in authorship["institutions"]:
                    inst_name = inst.get("display_name", "")
                    institutions[inst_name] = institutions.get(inst_name, 0) + 1 / num_insts

            matched.append({
                "PaperId": data["id"],
                "PaperTitle": data["display_name"],
                "Year": data["publication_year"],
                "CitationCount": data["cited_by_count"],
                "EstimatedCitation": data["cited_by_count"],
                "Affiliations": institutions,
                "Authors": [a["author"]["display_name"] for a in data["authorships"]]
            })
        return matched
    else:
        return []


# Function to process papers for a specific venue and year range
def get_information_for_venue_papers(venue, venuetype, yearrange=yearrange, force=False):
    filter_f = filter_journals if venuetype == "journal" else filter_by_header_and_page_number_keep_missing
    for year in yearrange:
        # print(venue, year)
        in_filename = dblp_raw_filename(venue, year)
        out_filename = filtered_papers_filename(venue, year)

        # Skip if raw data doesn't exist
        if not os.path.exists(in_filename):
            print(in_filename, "does not exist!")
            continue

        # Skip if already processed unless forcing reprocess
        if os.path.exists(out_filename) and not force:
            continue

        # Load raw paper data
        with open(in_filename, "r") as fh:
            papers = json.load(fh)

        # Apply filtering based on the venue type
        papers, _ = apply_filter_to_papers(filter_f, papers, venue, year)
        print(venue, year, len(papers))

        # If no papers after filtering, create an empty file
        if len(papers) == 0:
            with open(out_filename, "w") as fh:
                json.dump([], fh)
            continue

        output = []
        # Process each paper
        for row in papers:
            paper = {
                "DBLP title": row["title"],
                "DBLP authors": row["authors"],
                "year": row["year"],
                "doi": row["doi"],
                "OA papers": get_openalex_paper_info(row)
            }
            output.append(paper)

        # Save filtered papers to output file
        with open(out_filename, "w") as fh:
            json.dump(output, fh)

    print(venue)
    return None


# Helper function for retrying papers that missed OpenAlex data
def try_again_venue_papers(venue, venuetype, yearrange=yearrange, force=False):
    for year in yearrange:
        out_filename = filtered_papers_filename(venue, year)
        with open(out_filename, "r") as fh:
            papers = json.load(fh)

        # Retry for papers without OpenAlex data
        if len(papers) == 0:
            with open(out_filename, "w") as fh:
                json.dump([], fh)
            continue

        try_again = sum(1 for p in papers if len(p["OA papers"]) == 0)
        if try_again == 0:
            continue

        print(f"{venue} {year} {try_again}/{len(papers)} do not have OA papers. trying again...")
        output = []
        for paper in papers:
            if len(paper["OA papers"]) == 0:
                time.sleep(1)
                paper["OA papers"] = get_openalex_paper_info_title_search({"title": paper["DBLP title"]})
            output.append(paper)

        # Save updated papers with retries
        with open(out_filename, "w") as fh:
            json.dump(output, fh)

    return None


# The get_information_for_venue_papers_add_additional_papers function can be used to add additional filtered papers to a venue,year pair that has been affected by a change in the raw papers scraped or the filtering system without having to regather the information for the exisitng papers.
def get_information_for_venue_papers_add_additional_papers(venue, venuetype, year):
    
    filter_f = filter_journals if venuetype == "journal" else filter_by_header_and_page_number_keep_missing

    in_filename = dblp_raw_filename(venue,year)
    out_filename = filtered_papers_filename(venue,year)
    
    with open(in_filename, "r") as fh:
        papers = json.load(fh)

    papers, _ = apply_filter_to_papers(filter_f, papers, venue, year)
    
    with open(out_filename, "r") as fh:
        output = json.load(fh)

    original_output_size = len(output)
    existing_papers = [(paper["DBLP title"],paper["year"]) for paper in output]
    additional_papers = [paper for paper in papers if (paper["title"],paper["year"]) not in existing_papers]
    
    if len(additional_papers) == 0:
        print(venue,year,"nothing to add")
        return

    additional_output = list()
    for row in additional_papers:
        paper = dict()
        paper["DBLP title"] = row["title"]
        paper["DBLP authors"] = row["authors"]
        paper["year"] = row["year"]
        paper["doi"] = row["doi"]
        paper["OA papers"] = get_openalex_paper_info(row)
        additional_output.append(paper)

    output.extend(additional_output)
    
    final_output_size = len(output)

    with open(out_filename,"w") as fh:
        json.dump(output,fh)
    print(venue,year,"from",original_output_size,"to",final_output_size)

    return None


# Multiprocessing task function to run in parallel
def task(venues):
    for venue, venuetype in venues:
        # get_information_for_venue_papers(venue, venuetype)
        try_again_venue_papers(venue, venuetype)
    return None

def additional_papers_task(venues):
    for venue, venuetype, year in venues:
        get_information_for_venue_papers_add_additional_papers(venue, venuetype, year)
    return None


# Helper function to divide the workload across threads
def get_pool_lists(ls, threads):
    ls_ = ls.copy()
    if type(ls_) != list:
        ls_ = list(ls_)
    pool_lists = []
    list_size = len(ls) // threads
    for _ in range(threads - 1):
        pool_lists.append([ls_.pop() for _ in range(list_size)])
    pool_lists.append(ls_)
    return pool_lists


# Run tasks in parallel pools
def run_pools(task, lists, agg_f=None):
    pool = Pool(processes=threads)
    result = [pool.apply_async(task, (x,)) for x in lists]

    if agg_f is None:
        agg_f = lambda x: None
    for rs in result:
        agg_f(rs.get())
    pool.close()


# Main execution block for parallel processing
if __name__ == '__main__':
    start = datetime.now()

    # Load venues from CSV file
    venues = []
    with open(venue_category_filename, "r") as fh:
        reader = csv.reader(fh, delimiter=",")
        next(reader)  # Skip header row
        for row in reader:
            venue_type = row[4]
            name = row[0]
            venues.append((name, venue_type))

    # Divide venues across threads and run tasks
    pool_lists = get_pool_lists(venues, threads)
    run_pools(task, pool_lists)

    # venues = []
    # with open("single_page_number_exclusions.csv","r") as fh:
    #     reader = csv.reader(fh,delimiter=",")
    #     next(reader)
    #     for row in reader:
    #         key = row[0]
    #         year = int(row[1])
    #         venue_type = row[-1]
    #         venues.append((key,venue_type,year))
    # additional_papers_task(venues)

    print((datetime.now() - start).total_seconds())
