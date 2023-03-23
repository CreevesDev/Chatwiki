from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.error import URLError
import re


def get_papers(question, number=1):
    """
    Searches Google Scholar for papers related to the specified question and returns a list of up to `number` papers.
    :param question: The question to search for.
    :param number: The maximum number of papers to return (default is 1).
    :return: A list of up to `number` papers, each represented as a tuple containing the paper's title and authors.
    """
    url = f'https://scholar.google.com/scholar?q=' + question.replace(" ", "+")
    req = Request(
        url=url,
        headers = {'User-Agent':'Mozilla/5.0'}) #Required to bypass Google anti-spider 
    try:
        response = urlopen(req).read()
    except URLError as e:
        print(f"Error opening this URL: {url}, reason: {e.reason} ")
        results = [{"title": "Error", "authors": "N/a"}]
        return results
    soup = BeautifulSoup(response, 'html.parser')
    search_results = soup.find_all('div', {'class': 'gs_ri'})
    results=[]
    for search_result in search_results[:number]:
        title_a = search_result.find('h3', class_="gs_rt").find('a')
        title = title_a.text.strip()
        authors_div = search_result.find('div', class_="gs_a")
        authors = " ".join(authors_div.text.strip().split(' ')[::2]) + " et al."
        paper = (cleanse(title), cleanse(authors))
        results.append(paper)
    return results

def cleanse(t):
    return re.sub(r'[^A-Za-z0-9 ]+', '', t)