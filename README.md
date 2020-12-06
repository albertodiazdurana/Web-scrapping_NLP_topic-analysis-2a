- [I-E7.2](#i-e72)
  - [Environment setup](#environment-setup)
  - [Data scrapping](#data-scrapping)
    - [Run the code](#run-the-code)
# I-E7.2
I&E challenge Market analysis using IT tools - team 7.2

## Environment setup

The code is tested and developed in python 3.6.9. To setup your python environment, you need the following packages. 

- requests
- bf4
- pandas
- html5lib
- tqdm

Install using `pip install <package-name>`

## Data scrapping

The website <http://www.e-mfp.eu/who-s-who> has a list of micro-finance organisations, and includes general information, contact person, and summary for each orgnaisation listed. The goal here is to extract all those details about each organisation in a tabular form using beatifulsoup library in python.

### Run the code

On a command line type: `python3 scrapping.py`
After running the code, you will find the detailed organisation data in `org_info.csv` file.