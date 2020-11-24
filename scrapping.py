import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


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

    for tag in soup.find_all("li", {"class": "pager-item"}):
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
      urls(list(str)): urls of all individual organisations

      '''
    assert(type(webpages) == list)

    urls = []

    for i, page in enumerate(webpages):

        print('Fetching urls on page ', i+1)
        soup = webToSoup(page)

        for td_tag in soup.find_all("td", {"class": "views-field views-field-field-full-name"}):

            a_tag = td_tag.find("a")
            org_link = a_tag.get('href')
            urls.append(urljoin(page, org_link))

    return urls


def main():

    # mfp organisation page
    mfp_org_page = 'http://www.e-mfp.eu/who-s-who'

    # get sub pages where organisations are listed
    sub_pages = getSubPagesLinks(mfp_org_page)

    # get links of all those organisations
    org_links = getOrganisationsLinks(sub_pages)

    print('Total organisations links: ', len(org_links))
    print('\n', org_links)


if __name__ == "__main__":
    main()
