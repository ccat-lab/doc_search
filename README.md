Document Search Notebook
========================

doc_search is a small toolkit providing a Jupyter Notebook widget that can assist 
in directed search for specific documents related to specific universities. It was
originally built to aid in the search and download of annual from 20 universities.

Installation and use
--------------------

### Download

Most users will probably find it easiest to download a python distribution that 
includes Jupyter notebooks. [Anaconda](https://www.anaconda.com/download/) is a popular 
andfree choice that includes all the necessary libraries. It is also the distribution 
that we have used.

Download the repository as a directory. The notebook also requires a JSON dump from the 
GRID database. This is provided in the
form of a September 2017 data dump. You can replace this with the most up to date
data from [the GRID website - https://grid.ac/downloads](https://grid.ac/downloads).
You only need the JSON file `grid.json` from that archive.

### Preparation

The notebook will need a file containing a list of 
universities that you want to analyse. An example is provided as the file 
`example_uni_list.csv`. This file
*must* contain a column titled `id` which contains ids from GRID. All other columns
are optional. We include a name for convenience in our work and sometimes other
information as necessary.

Finally, you will need to obtain a Bing API key for running the searches. For small 
scale work and testing you should be able to get a new account with a reasonable number 
of free calls. If you scale up you may find you need to pay a small amount but most of 
our work hasn't hit that threshold. You can get an API key at: 
https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/ 
and select the 'Try Bing Web' option and then 'Free Azure Account'. You should 
ultimately get a key, which needs to be added at the top of the file 
`doc_search/doc_search/search.py` on the line that says:

`subscriptionKey = "subscriptionKey" <---change the second bit with your key that looks like 87dg7654has237`

### Opening and use

Use Anaconda (or your preferred Jupyter approach) to open a Jupyter notebook server.
Navigate to the downloaded folder in the Jupyter browser and open the 
notebook `Example Notebook.ipynb`. Further instructions are also contained in the 
notebook.

You may want to change the folders specified in the first code box. You should 
definitely change the filename for the output files. You *must* execute each cell 
either by clicking in it and selecting `run` from the toolbar, or by typing 
`SHIFT-Enter` while the cursor is in the cell.

### Search term setup

There are a range of options here and the full set of Bing advanced search operators 
should be available. A particularly useful option is filetype:pdf for pdf documents. 
Any text that needs to be searched for exactly should be enclosed in double quotes as 
for "library access policy" below. 

Note that by default the search will be limited to the URLs that GRID is aware of for 
the university. If your target documents are not on the university domain they may not 
be found. If you want to turn this off then change the second line in the cell below to 
read as follows:
`includeuniurl = False`

In addition to the Bing options it is also possible to include elements from the GRID 
data for the university. These need to be included inside a pair of curly braces as 
is shown for {name} in the notebook which will insert the university's name from the 
GRID data. Only those elements of the GRID JSON with a top level text entry will provide 
sensible results. These options include:

* {name} - the university's full name
* {id} - university's GRID ID
* {wikipedia_url} - university's wikipedia URL
* {established} - the date of the university's founding

### The search widget

This is the main part of the notebook. When you execute this cell a window should 
appear with search results for your first university. There may be up to 5 results 
depending on what Bing finds. You can select as many of the results as you wish using 
the buttons below the window. Clicking again will clear a button and hitting 'None' 
will clear all the buttons. 'Next' and 'Previous' move to the next and previous 
university respectively. 

Your selection and some further information for each university will be written to
an output file with the name and location that you set at the top of the notebook. 
Behaviour with the 'Previous' button is not always exactly as expected so avoid unless 
necessary. It should however be possible to just keep adding to the output file which 
should not overwrite previous results. The progress bar will tell you how far through 
a set of results you are.

Once you have run through a set of universities you can change the search term 
(remembering to `run` the cell after doing that) and run the search widget again by
running the cell which activates it. You can do this as many times as you like and 
the results should always be written to the output file for later inspection. 

### Downloading files

The search widget does not download files. The cell at the bottom of the notebook
will work through the output file and download all the target files that have been
selected. If there is a failure it is possible to re-run this cell. It should only
download files that are not already there. 

This means you can also change the search term, run additional searches and download
further files if you want to.


