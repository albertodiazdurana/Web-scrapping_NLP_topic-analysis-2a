import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from os import path
from tqdm import tqdm


def webToSoup(webpage):
    ''' Convets a webpage to a beautiful soup object

    Parameters:
    -----------
    webpage(str): url of the webpage

    Returns:
    ----------
    soup(BeautifulSoup): beauriful soap object of the webpage

    '''

    # access the webpage
    result = requests.get(webpage)

    # check if the webpage is present
    assert(result.status_code == 200)

    # return the content of webpage
    src = result.content

    # parse and process the source using Beautiful Soup object
    soup = BeautifulSoup(src, 'lxml')

    return soup


def getSubPagesLinks(base):
    ''' Get all subpages links listed on the webpage

    Parameters:
    -----------
    base(str): url of the first webpage (page with a multiple sub pages)

    Returns:
    ----------
    urls(list(str)): urls of all subpages

    '''

    soup = webToSoup(base)
    urls = [base]

    for tag in tqdm(soup.find_all("li", {"class": "pager-item"}), desc="Collecting sub pages..."):
        a_tag = tag.find("a")
        pageurl = a_tag.get('href')
        urls.append(urljoin(base, pageurl))

    return urls


def getOrganisationsLinks(webpages):
    ''' Get links of organisations listed on webpages

      Parameters:
      -----------
      webpages(list(str)): url of the pages where organisations are listed

      Returns:
      ----------
      urls(list(str)): urls of all individual organisations.
      Also save them in a 'org_links.csv' file
      '''
    assert(type(webpages) == list)

    urls = []

    for i in tqdm(range(len(webpages)), desc="Collecting org links..."):

        page = webpages[i]
        soup = webToSoup(page)

        # organisation links are in the <td> tag
        for td_tag in soup.find_all("td", {"class": "views-field views-field-field-full-name"}):

            a_tag = td_tag.find("a")
            org_link = a_tag.get('href')
            # join home page and relative link
            urls.append(urljoin(page, org_link))

    # save the links to a file so that it can reused without having to search for links each time
    df = pd.DataFrame(urls, columns=['Organalisation links'])
    df.index += 1  # as index starts from 0, adding 1 makes it start from 1
    df.to_csv('org_links.csv')

    return urls


def extractOrganisationInfo(webfile):
    ''' Scrap the data from organisational webpages in a tabular form

    Parameters:
    -----------
    webfile(.csv file): .csv file containing url of the individual organisations 

    Returns:
    ----------
    df: DataFrame consisting all organisational info in tabular form.
    Also saves the data in 'org_info.csv' file

    '''
    df_link = pd.read_csv(webfile)

    webpages = df_link['Organalisation links']

    df = pd.DataFrame(columns=[], dtype="string")

    # each webpage data is represented as a row in the data frame
    for i in tqdm(range(len(webpages)), desc="Scrapping org info ..."):

        url = webpages[i]
        soup = webToSoup(url)

        # the three major blocks of text namely {Organisation general information, Organisation's contact person, Organisation summary}
        #  are represented using filedset tags
        tags = soup.find_all("fieldset")

        for tag in tags:

            # rows in a block are inside div tag with class field
            for row in tag.find_all("div", {"class": "field"}):

                # left hand columns in the blocks are defined by div tag with class field-label
                label_tag = row.find("div", {"class": "field-label"})

                # left hand columns in the blocks are defined by div tag with class field-items
                item_tag = row.find("div", {"class": "field-items"})

                # add the item in the dataframe
                df.at[i, label_tag.get_text()] = item_tag.get_text()

    df.index += 1  # as index starts from 0, adding 1 makes it start from 1

    df.to_csv('org_info.csv')
    return df


def main():

    # file containing organisations links for which data scrapping has to be done
    weblinks_file = "org_links.csv"

    # if file not present, create the file by scrapping the website links
    if not path.exists(weblinks_file):

        print('org_links.csv file not found! Making one ...\n')
        # mfp organisation page
        mfp_org_page = 'http://www.e-mfp.eu/who-s-who'

        # get sub pages where organisations are listed
        sub_pages = getSubPagesLinks(mfp_org_page)

        # get links of all those organisations
        org_links = getOrganisationsLinks(sub_pages)

        print('Total organisations links: ', len(org_links))
        # print('\n', org_links)

    # extract the org. info
    extractOrganisationInfo(weblinks_file)

    print("\nDone")


if __name__ == "__main__":
    main()
