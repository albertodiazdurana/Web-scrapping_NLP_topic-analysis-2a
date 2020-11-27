- [I-E7.2](#i-e72)
  - [Environment setup](#environment-setup)
  - [Data scrapping](#data-scrapping)
    - [Approach](#approach)
    - [Run the code](#run-the-code)
# I-E7.2
I&E challenge Market analysis using IT tools - team 7.2

## Environment setup

The code is tested and developed in python 3.6.9. To setup your python environment, you need the following packages. 

- requests
- bf4
- pandas
- tqdm

Install using `pip install <package-name>`

## Data scrapping

The website <http://www.e-mfp.eu/who-s-who> has a list of micro-finance organisations, and includes general information, contact person, and summary for each orgnaisation listed. The goal here is to extract all those details about each organisation in a tabular form using beatifulsoup library in python

### Approach
   There are total of 9 subpages listed on the website, each containing around ~12 orgnisations urls.
   1. Firstly, we extract the urls of all those 9 subpages.
   2. We then visit each subpage, and extract urls of all organisation listed on that subpage. Finally, after visiting all subpages we have urls of each organisation listed on the website. These links are also saved in a csv file named `org_links.csv`.
   3. We visit each organisation page, scrap all the data in a tabular form and save it in `org_info.csv`.

### Run the code

On a command line type: `python3 scrapping.py`
After running the code, you will find the detailed organisation data in `org_info.csv` file.