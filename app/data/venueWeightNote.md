## Venue Weight Computation 

The result of the process described below are stored in `venue_weight.csv` (containing arithmetic mean, geometric mean and 80th percentile). We use the geometric mean for our calculations.

### Background

Not all venues are equally prestigious.  Considering only the most prestigious venues may be appropriate for the top departments, but risks having very small numbers influence the score obtained for lower ranked schools.  Therefore, we include several hundred venues, but recognize that publication in some is worth more than publication in others.

We could weight venues subjectively.  For example, we could put them in a few categories, and assign different amounts of credit for each category.  While that may be a reasonable scheme, we chose to let citation data drive venue weights.

Specifically, we considered the number of citations to each paper published in that venue in the past 10 years.  The average number of such citations is the venue weight.  For a new paper published at this venue, this number is an estimate of the number of citations we can reasonably expect, on average.  Therefore, it is an appropriate estimate of the citation score that this paper will eventually have.

### Geometric mean

One question of detail is what type of average to compute.  With arithmetic mean, we find that a few heavy hitters dominate: the impact of most other papers on the average is limited.  With geometric mean, the contribution of each paper matters more, including those with low numbers of citations.
Therefore, we use the geometric mean for our calculations.

One difficulty with the geometric mean is that it is undefined when the number of citations is zero.  There indeed are some papers with zero citations.  To handle this case, we add 1 to the number of citations before computing the geometric mean, and then subtract 1 from the mean obtained.

