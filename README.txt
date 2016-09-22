This will create an HTML page based on template.html

Required libraries:
    BeautifulSoup4
    requests
    urlparse
    datetime

Make sure that template.html is in the same directory as this script or change the path to the template file by finding ### Change me to the path to the template file ### and changing the variable underneath.
If you would like to change the amount of search results retrieved, find ### Change this to change how many results are displayed ### and change the variable underneath.

The images are retrieved by taking the title of the page, and doing a Google Image search on it, and using the first result.

Once run, you will prompted to enter a search query.
The new HTML page will be created, and named after the search term, and today's date.
