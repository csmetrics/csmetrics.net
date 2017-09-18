# Institutional Publication Metrics for Computer Science

## Frequently asked questions

### 1. What is a measured versus a predicted metric?

Publications usually take several years to accumulate citations.  For older publications, citation count is a measure of impact.  This is what we use as a measured metric.

For newer publications, it is not reasonable to count citations.  Rather, we must predict how many citations the paper may accrue, given time.  For this purpose, we have computed the (geometric) mean number of citations per full research paper in each venue, computed over the last ten years.  If the venue, and the sub-field it represents, remains unchanged, we should expect an average paper published at the venue today to have this mean number of citations eventually.  These are the default venue weights we provide.


### 2. What is with the geometric mean?

When numbers differ widely in scale, the arithmetic mean tends to ignore the smaller numbers and be driven only by the larger ones.  The geometric mean is more equitable.


### 3. What can I do if I do not like your choice of venue weights?

At the current time, you can choose between our suggested (geometric mean citation count) venue weight and an equal venue weight (of 1) for all venues.  You can also choose to include or exclude each venue, effectively setting the weight to zero.  At the current time, these are your only choices.  In the future, we hope to allow you to choose your own venue weights.
Keep in mind that venue weights only affect predicted scores.  Measured scores are based purely on actual citation counts.


### 4. You include too many venues I think should not be counted.  What can I do?

You can individually toggle each venue, to include or exclude it.  To make this easier for you, we have grouped venues into rough sub-areas of Computing.


### 5. You are missing venues I think should be counted.  What can I do?

Please [submit a request](https://github.com/csmetrics/csmetrics.org/issues).  If we can, we will include this venue, and the data associated, at the next release of our tool.


### 6. Why are we combining measured and predicted scores?

We suggest that you set alpha to an extreme value (0 or 1) to see scores based purely on measured historical reputation and separately scores based on recent productivity.  You could fold these together subjectively, if you wish.  If you wish to combine these two different scores mathematically, we provide you with the alpha value slider.
