README.txt

This module requires the use of Python 3.X preferably something later than Python 3.5.

INSTALL
Before starting the module, make sure that your current python environment has the following modules:
• requests
• bs4
• os
• pathlib
• tqdm
• tkinter
• dateutil
• urllib

To check whether or not you have a module, run your python environment and enter "import <module_name>"

>>> import <module_name>
>>>

If successful you should get a new line. 
If not successful you will receive an error message.

To install any missing module, I recommend using "pip install"

From the cmd line:

> py -m pip install <module_name>

If you don't have pip please Google how to obtain pip for you python environment.

USING THE SCRAPER
Once you have successfully checked that all modules are installed, go ahead and run your python environment:

> py

You should have the module, bsScrape.py, saved to your "<python environment>/Lib/" folder before continuing. 

Once in your python environment import bsScrape:

>>> import bsScrape
>>>

You should have a new line appear under your import line.

To start scraping "https://app.hedgeye.com/insights/all?type=insight" just run the scrape function:

>>> bsScrape.scrape()

The function already has "https://app.hedgeye.com/insights/all?type=insight" as the default url.

As it is running, a folder dialog browser will prompt you for the directory that you would like to store the csv files to.

Please select a folder.

A progress bar will show up in the terminal as an indicator for you.

Once done, the folder will be populated by subfolders containing the csv scrapings and the first image of the page, if available.

CAVEAT
Unfortunately, the links provided do not contain sufficient information to post author details as required.

To verify that the program works according to specs we will have to do the following:

I had to search for a page that contained author details. The one that I found was "Bull Market Math" with a url: "https://app.hedgeye.com/insights/56097-bull-market-math?single_item=true".

Instead of calling the scrape function, we will instead call the writeToFolder function as demonstrated:

>>> import bsScrape
>>> folder = bsScrape.getFolderpath()
>>> bsScrape.writeToFolder("https://app.hedgeye.com/insights/56097-bull-market-math?single_item=true",folder)
>>>

We used the getFolderpath function to make it easier to choose where we want the output to go.

The folder created will contain a csv file with the correct author information and the first available image.
