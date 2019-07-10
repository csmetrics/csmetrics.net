

minimum_page_length = 4

def get_page_length(pagination):
    
    try:
        int(pagination)
        return 1
    except:
        pass

    if (pagination == None) or ("-" not in pagination):
        return None


    try:
        pagination = pagination.split("-")
        
        # deal with page numbers with the format chapter:firstpage-chapter:lastpage
        if ":" in pagination[0]:
            start = int(pagination[0].split(":")[1])
            end = int(pagination[1].split(":")[1])
        else:
            start = int(pagination[0])
            end = int(pagination[1])
            
        page_length = end - start + 1

    except:
        return None
    
    return page_length


def filter_by_header(header, paper):
    
    # these have to exactly match a token after header.split()
    # explanation: because these words were found to be prefixes or suffixes
    #              to sections that should not have been excluded
    filterwords = ['demo']#, 'short', 'oral']
    
    # these can match any substring in header
    filterphrases = ['senior member',"what's hot", "invited",# 'poster', 
                     'doctoral', 'demonstration', 'keynote', 'student',
                     'speaker', 'tutorial', 'workshop', 'panel',
                    "competition", "challenge"]
    
    header = header.lower()
    
    exclusions = [filterword for filterword in filterwords if filterword in header.split()]
    exclusions +=  [filterphrase for filterphrase in filterphrases if filterphrase in header]
    
    # if no word or phrase to exclude on
    if len(exclusions)==0:
        return True
    
    else:
        return "keyword in header: " + ", ".join(exclusions)

    

def filter_by_header2(header, paper):
    
    # these have to exactly match a token after header.split()
    # explanation: because these words were found to be prefixes or suffixes
    #              to sections that should not have been excluded
    filterwords = ['demo']#, 'short', 'oral']
    
    # these can match any substring in header
    filterphrases = ['senior member',"what's hot", "invited",# 'poster', 
                     'doctoral', 'demonstration', 'keynote', 'student',
                     'speaker', 'tutorial', 'workshop', 'panel',
                    "competition", "challenge"]
    
    header = header.lower()
    
    exclusions = [filterword for filterword in filterwords if filterword in header.split()]
    exclusions +=  [filterphrase for filterphrase in filterphrases if filterphrase in header]
    
    # if no word or phrase to exclude on
    if len(exclusions)==0:
        return True
    
    else:
        return "keyword in header: " + ", ".join(exclusions)
    
    
    
def filter_by_page_number_keep_missing(header, paper):
    global minimum_page_length
    
    page_length = get_page_length(paper["pagination"])
    
    if page_length == None or page_length >= minimum_page_length:
        return True
    
    else:
        return "page length {} is less than mimumim {}".format(page_length, minimum_page_length)
    
    
def filter_by_page_number_remove_missing(header, paper):
    global minimum_page_length
    
    page_length = get_page_length(paper["pagination"])
    
    if page_length == None:
        return "no page numbers"
    
    elif page_length >= minimum_page_length:
        return True
    
    else:
        return "page length {} is less than mimumim {}".format(page_length, minimum_page_length)
    

def filter_by_header_and_page_number_keep_missing(header, paper):
    global minimum_page_length
    
    header_filter = filter_by_header(header, paper)
    
    if header_filter != True:
        return header_filter
    
    else:
        return filter_by_page_number_keep_missing(header, paper)
    

def filter_by_header_and_page_number_remove_missing(header, paper):
    global minimum_page_length
    
    header_filter = filter_by_header(header, paper)
    
    if header_filter != True:
        return header_filter
    
    else:
        return filter_by_page_number_remove_missing(header, paper)

    
def filter_journals(header, paper):
    global minimum_page_length
    
    filterphrases = ['editor', 'special issue','state of the journal', 'in memory']
    
    title = paper["title"]
    title = title.lower()
    
    exclusions =  [filterphrase for filterphrase in filterphrases if filterphrase in title]
    
    # if no word or phrase to exclude on
    if len(exclusions)==0:
        return filter_by_page_number_keep_missing(None, paper)
    
    else:
        return "keyword in title: " + ", ".join(exclusions)

    
def apply_filter_to_papers(filter_f, papers):
    included_papers = list()
    excluded_papers = list()
    
    for header, section_papers in papers.items():
        for paper in section_papers:
            filter_result = filter_f(header, paper)

            # for included papers
            if filter_result == True:
                included_papers.append(paper)

            # for excluded papers pair them with reason for exclusion
            else:
                excluded_papers.append((paper, filter_result))
    
    return included_papers, excluded_papers
