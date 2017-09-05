# Motivation

Rankings highly influence students, faculty members, and institutions.   Whether Computer Science wants to be ranked or not, it will be ranked.  

We seek to improve the quality of data and analytical tools available to Computer Science (CS) deans, chairs, faculty, students, departments, institutions, such that they can inform decision making and ranking activities by combining quantitative metrics with expert qualitative opinions, recognizing that the data and metrics will never be perfect.  

Although judging research quality is hard, science judges itself and scientific progress, almost universally,  by combining expert qualitative opinion with quantitative metrics.  Our tool focuses on quantitative publication metrics for 2007-2016.  Because all big data is dirty, we spent considerable time cleaning the data we gathered from [dblp](http://dblp.uni-trier.de) and [Microsoft Academic Scholar](http://academic.research.microsoft.com) which sources its data from ACM, IEEE, and other publishers. We clean publication venue, citations, and institutional data for over XXX conferences and journals.  We describe our data cleaning process and metrics in more detail below in [Methodology](#methodology).  

University research, like so many other accomplishments, is complex and multi-dimensional, and hence hard to measure.  In addition, many things we care about, such as impact, reputation, and alumni success, take time to manifest themselves.  In consequence, it is hard to know how well an institution is doing at present, or to determine whether an institution is on an upward or a downward trajectory.

In this paper, we address the above challenges, while restricting our focus to scholarly publications.    

In this paper, we develop a simple model that predicts the future citations of a paper at the time of its publication, and use this to get a less backward-looking metric of institutional accomplishment, at least in terms of Computing-related publications.
using a retrospective metric (citations) and a predictive metric (for very recent publications; each publication may be weighed by a measure of venue strength).

[Below](#other) we describe how our approach differs from efforts such as [U.S. News & World Report](https://www.usnews.com/best-graduate-schools/top-science-schools/computer-science-rankings), which only uses opinions, [Computer Science Rankings (beta)](www.csrankings.org), which counts papers in selected venues for current faculty, and [Scholar Ranking](http://www.dabi.temple.edu/~vucetic/CSranking/), which uses citations and productivity for current faculty.  In particular, rather than individual faculty’s credit moving with them if they move, we focus on institutional metrics that credit all authors with work performed at an institution. Publications never change institutions.  We use both retrospective and predictive metrics.

Publications, and citations to these publications, are time-honored ways in which to quantify research accomplishments.  While these metrics are not perfect, they are the best we have in terms of available and relatively well curated data, and are likely to be substantially superior to subjective guesses.  We note that our tool is incomplete because it does not include other important metrics, such as, count of faculty, research test-of-time awards, faculty honors, PhD placement, and funding. Some of these metrics are available elsewhere, but for now they are outside our scope.

# Table of Contents
* [Methodology](#methodology)
* [Cleaning the data](#cleaning)
* [Metrics](#metrics)
* [Limitations](#limitations)
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

## <a name="limitations"></a>Limitations

As discussed above, we only consider publications, which are a very important piece of scolarly output, but still only a piece.  Even when considering publications, we ideally wish to measure impact rather than just count publications.  We use citations as the measure of impact, but recognize that citations do not tell the full story.

A significant challenge with using citations as a metric is that citations take time to accumulate, with significant variation across papers in citation rate over time.  As such, citations are not a good way to measure impact for recent papers, less than 2 or 3 years old.   We have developed and used a novel metric, based on predicted citation count, estimating this based on the venue.  There is room to improve this metric, by performing a  more careful estimation, taking into account not just venue but also the author(s) and their institution(s).

We note that the longer ago a paper was published and, similarly, the older a particular instance of a venue,  the more time they have to accrue citations.  Thus, both citations and venue weights are influenced by time, and, furthermore, publication and citations practices change over time.  As an example,  a number of venues recently eliminated page count limitations on citations.   A limitation of our current tool is that it does not consider this time varying component of the data.

In our tool, credit goes to institutions based on authors affiliation(s) at time of publication and never changes.  But people move.  If a professor moves from institution A to institution B, it can be argued that B should now get (some of) the credit for the work they did while at A.  But it can equally be argued that credit should remain with the institution where the work was done, after all that was the environment that supported and enabled the work.  Certainly, students should not carry away with them credit for work they did at an institution that trained them.  Furthermore, institutions should not be able to “buy”  credit by hiring famous faculty past their prime.  While both these views have merit, we have chosen to adopt an immovable credit methodology, because we know we can do it correctly.  Having credit move requires considerable work tracking individual authors, and determining their individual career stages, which we have not undertaken.

More people obviously can get more done.  When we score numbers of publications, citations, and so on, we expect larger institutions to have larger scores.  If we could get a good count for the size of an institution, this count could be used to obtain a normalized per person score.  However, as discussed above, it is not straightforward to count correctly the number of people to divide by: should it be faculty, research faculty, or tenure-track faculty?  Should number of students (and post-docs/fellows) play a role?
A better way to address this problem, which we hope to do in the future, is to compute the score individually for faculty affiliated with an institution.  We can then report the score for the kth ranked professor for different values of k.  The higher this score, and the deeper the bench of star faculty with high scores, the stronger the institution.  

The publications data we have obtained and cleaned is only for selected publications, of necessity.  For publications related to computing, we have tried to include most international forums.  Depending on your perspective, you may choose to leave out some of these in your analysis, and the tool supports your doing this.  If venues you care about are missing, please do let us know.

Interdisciplinary work is to be applauded, and is encouraged by many.  Yet, it is difficult to measure well.  With our methodology, popular venues outside the core of computing are included, to cover some amount of broadening.  However, venues completely outside Computing are not included, even if very prestigious.  Thus, for example, publications in Nature do not count.  The reason is that most publications in Nature have nothing to do with Computing.  So including Nature in our statistics will primarily reflect work by people unrelated to Computing.  

Many venues have multiple classes of publications: for example full papers and short papers.  Our present system only includes what we considered to be full refereed research papers.  However, some short papers at very prestigious venues may be more important and impactful than full papers at less selective venues.  In future work, we plan to consider such short papers also.

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
