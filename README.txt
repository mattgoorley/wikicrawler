Make sure to check requirements.txt for packages.


Write a program using Python that performs the following:Take any random article on Wikipedia (example: http://en.wikipedia.org/wiki/Art) and click on the first link on the main body of the article that is not within parenthesis or italicized; If you repeat this process for each subsequent article you will often end up on the Philosophy page.Questions:•  What percentage of pages often lead to philosophy?•  Using the random article link (found on any wikipedia article in the left sidebar),what is the distribution ofpath lengths for 500 pages, discarding those paths that never reach the Philosophy page?•  How can you reduce the number of http requests necessary for 500 random starting pages?   


Questions answered:

1. What percentage of pages often lead to philosophy?

A: 92.2%


2. Using the random article link (found on any wikipedia article in the left sidebar),what is the distribution of
path lengths for 500 pages, discarding those paths that never reach the Philosophy page?

A: Please see the plot.png for the distribution. It looks to be non-symmetric, bimodal with the two medians being 8 and 15.

3. How can you reduce the number of http requests necessary for 500 random starting pages?

A: We can reduce the number of http requests by cacheing each request made with its path to the Philosophy page. At any future point if we hit that page again we can stop making requests because we know that page's path. We hit many pages multiple times so this would greatly reduce http requests over time.

