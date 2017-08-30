# Motivation

Rankings highly influence students, faculty members, and institutions.   Whether Computer Science wants to be ranked or not, it will be ranked.  

We seek to improve the quality of data and analytical tools available to Computer Science (CS) deans, chairs, faculty, students, departments, institutions, such that they can inform decision making and ranking activities by combining quantitative metrics with expert qualitative opinions, recognizing that the data and metrics will never be perfect.  

Although judging research quality is hard, science judges itself and scientific progress, almost universally,  by combining expert qualitative opinion with qualitative metrics.  Our tool focuses on quantitative publication metrics for 2007-2016 using a retrospective metric (citations) and a predictive metric (for very recent publications; each publication may be weighed by a measure of venue strength).  For both metrics, credit goes to institutions based on authors at time of publication and never changes.  Because all big data is dirty, we spent considerable time cleaning the data we gathered from [dblp](http://dblp.uni-trier.de) and [Microsoft Academic Scholar](http://academic.research.microsoft.com) which sources its data from ACM, IEEE, and other publishers. We clean publication venue, citations, and institutional data for over XXX conferences and journals.  We describe our data cleaning process and metrics in more detail below in [Methodology](#methodology).  

[Below](#other) we describe how our approach differs from efforts such as [U.S. News & World Report](https://www.usnews.com/best-graduate-schools/top-science-schools/computer-science-rankings), which only uses opinions, [Computer Science Rankings (beta)](www.csrankings.org), which counts papers in selected venues for current faculty, and [Scholar Ranking](http://www.dabi.temple.edu/~vucetic/CSranking/), which uses citations and productivity for current faculty.  In particular, rather than individual faculty’s credit moving with them if they move, we focus on institutional metrics that credit all authors with work performed at an institution. Publications never change institutions.  We use both retrospective and predictive metrics.

We note that our tool is incomplete because it does not include other important metrics, such as, count of faculty, research test-of-time awards, faculty honors, PhD placement, and funding. Some of these metrics are available elsewhere, but for now they are outside our scope.

# Table of Contents
* [Methodology](#methodology)
* [Cleaning the data](#cleaning)
* [Metrics](#metrics)
* [Other CS Ranking Methods and Tools](#other)
* [Short term plans and long term goals](#plans)


# <a name="methodology"></a>Methodology

We organize CS publication data by venue, author institution, and citations.   We currently have XXX conference and journal venues. Our intention is to include all CS venues with a rigorous peer-review process.  We currently present YYY institutions out of 5000+ that our tools identified as participating in CS research world-wide.  We intend to include them all eventually, but  because authors do not uniformly indicate their institution, we must hand-identify and encode institutional aliases. The next section first describes more on why and how we cleaned publication data, and then we describe our analysis and metrics based on this data.

## <a name="cleaning"></a>Data cleaning
We gathered publication data from 2007 to 2016 from … this data is all derived from publishers such as ...

Lots of publication data is available from DBLP, Google Scholar, Microsoft Academic, and publishers such as ACM and IEEE, but unfortunately as with all big data, this publication and citation data is dirty and some errors are orders of magnitude. Careful examination of ACM and IEEE publication data, and sources derived from them (e.g., dblp, Google Scholar, and Microsoft Academics) showed numerous systematic and one-off errors that resulted in orders of magnitude differences in publication counts for some venues.  For example, we found examples where all of the papers in a major conference (e.g., OOPSLA, ICSE)  with a rigorous peer review processes were grouped together with large numbers of unrefereed posters and publications at satellite workshops with a different submission and editorial processes.

### Cleaning publication to venue mapping

For each venue…

### Cleaning author to institution mapping 

Because sometimes the same author or authors from the same institution do not record the name of their department, University or other institute consistently, there are many institution names that should map to the same place.  These aliases deflate the publication statistics for an institution.  When we simply mine the publication data for institutional names, we get over 5,000 institutions world-wide.  To clean this data, we therefore first started by restricting ourselves to a smaller number. We chose the CRA institutions because most U.S. and Canadian active academic and industrial CS research institutions are members. We identified aliases by hand and with keyword search for these institutions. 

Because aliases cause under-reporting, we only include cleaned institutions. We plan to add more soon.

### Choice of venues

We chose to include XXX conference and journal venues. CS research topics, publication practices, and citations practices are changing rapidly.  For instance, new areas are emerging as interdisciplinary and CS research evolves and flourishes.  Including venues that primarily focus on other fields such as Science and Nature is not appropriate.  However, including new venues and small research areas to encourage and help emerging topics flourish is critical to rewarding interdisciplinary work and accelerating innovation. Choosing these venues requires qualitative judgements. 

The list of venues is available here. 

### Choice of research topics 

For each venue, we identified major topics it covers. The number of CS research topics is expanding and becoming increasingly interdisciplinary as computational methods are applied to new areas and in new ways.

Since publication and citation practices differ substantially by CS sub-area, we think qualitative analysis must complement bibliometrics by area. In the future, it may be possible to develop a methodology for grouping and analyzing sub-areas that informs combining and comparing subareas, but we leave those kinds of metrics for future work.

## <a name="metrics"></a>Metrics
We propose combining two metrics for the purposes of analyzing past research impact and trying to predict the future.  For past research impact, we use citations to publications. For prediction, we use paper counts and venue impact. 

We start by dividing credit for each paper equally among all authors and credit it to their institution. 

**Measured impact**  For each publication, we query Microsoft Academic API for all citations from any year. Each institution with an author then accrues these citations weighted by the fraction of authors at the institution. For example, a publication with 2 authors at University A and one author at University B and 100 citations, accrues 66.6 citations to University A and 33.3 citations to University B.

**Predicted impact**   More than other disciplines, CS research institutions are currently experiencing a lot of growth to meet student demand and societal workforce and innovation demands on CS.. We have thus included a predictive forward-looking metric, to understand the benefits of investment or the results of neglect.

For the predicted impact, we compute the number of papers appearing in a venue and divide the credit equally among authors’ institutions. We optionally weight this count by the geometric mean of the citations to the venue.  This weighting thus gives more potential impact to papers that appear in venues that in the past had more citations.  We use the geometric mean instead of the arithmetic mean because even in the impactful venues, many papers are not cited, many incur only a modest number of citations (which depend on the discipline and point in history), and a few are highly cited. ADD A CITATION.

**Limitations**  We note that the longer ago a paper was published and, similarly, the older a particular instance of a venue,  the more time they have to accrue citations.  Thus, both citations and venue weights are influenced by time, and, furthermore, publication and citations practices change over time.  As an example,  a number of venues recently eliminated page count limitations on citations.   A limitation of our current tool is that it does not consider this time varying component of the data.

# <a name="other"></a>Other CS Ranking metrics and tools

Unfortunately for CS, the most influential ranking source for CS graduate programs, The [U.S. News & World Report](https://www.usnews.com/best-graduate-schools/top-science-schools/computer-science-rankings), is based only on opinions. Our purpose is to influence rankings by metrics and opinions.  Our metrics have a different focus than two recent sources of rankings, [Computer Science Rankings (beta)](www.csrankings.org) and [Scholar Ranking](http://www.dabi.temple.edu/~vucetic/CSranking/), which evaluate current faculty.  In these systems, research impact is measured by faculty research. The research of PhD students, postdoctoral students, undergraduates, research staff, and collaborators in other departments at the same institution are not included.  If a faculty member moves between institutions, all their publications move with them. Our tool differs because all authors accrue credit to their institution at time of a paper’s publication and this credit is not moveable.   Depending on your purpose for ranking, faculty metrics and institutional metrics likely both have a place.

The [Computer Science Rankings (beta)](www.csrankings.org) tool uses publications counts for a small set of top venues, chosen in part based on venue average citation counts. It counts publications for current faculty with full-time tenure track appointments in the computer science department, school, or college.   While clearly the top venues by citation counts capture a lot of influential research publications, they do not always capture it.  Omitting many venues is problematic because it credits unlisted publications as worthless, making a very strong value judgement. It may further incentivize faculty to publish only in certain venues and discourage wider scientific participation. Limiting venues makes new, emerging areas very hard to capture or judge. 

Numerous prestigious international research organizations, including DORA, the UK Parliament, the European Association of Science Editors, the American Society for Biology and others,  recommend strongly against using venue as a proxy for quality.  For instance,  recommendation 1 of the DORA statement reads:  “Do not use journal-based metrics, such as Journal Impact Factors, as a surrogate measure of the quality of individual research articles, to assess an individual scientist’s contributions, or in hiring, promotion, or funding decisions.”   We note that recent publications, e.g., in the past two or three years do not have citations on which to judge them, so venue reputations based on past citations to publications in that venue provide one quantitative measure of potential impact. Our tool makes it possible to only focus on citations or to use papers in any venue or a weighted venue for recent work as a predictive metric, rather than an impact metric.  This forward-looking metric can help judge the direction of an institution, showing investments in faculty hiring, graduate student support, etc., or neglect.

[Scholar Ranking](http://www.dabi.temple.edu/~vucetic/CSranking/) uses citations of current faculty by querying Google Scholar for the number of citations to the faculty member’s 10th most cited paper (T10 metric).  They use the median and geometric mean then weigh it by faculty rank (full and associate professors are grouped together, and assistant professors are grouped separately).  They also weigh publication credit by author order, whereas we divide it equally since some areas use alphabetic and other conventions for author ordering.  The T10 metric rewards productivity as well as citations, but minimizes the impact of the very most influential papers that accrue many citations, which seems counter-productive to understanding impact.  However, they offer a number of metrics and weights, and find that their ranking correlates well with the U.S. News & World Report ranking.   

# <a name="plans"></a>Short term plans and long term goals

Journal ...
Institutions... 
Topics...
We believe that this activity should be supported and expanded with awards, current faculty members, funding, etc. by the community in perpetuity and welcome your participation. 
