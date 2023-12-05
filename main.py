import requests
from bs4 import BeautifulSoup

URL = "https://www.bfi.org.uk/industry-data-insights/weekend-box-office-figures"


def main():
    find_latest_file()


def find_latest_file():
    response = requests.get(url=URL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    latestFileLink = soup.find('a', {'class': 'FileDownload__Link-sc-ix3u4x-1'})
    print(latestFileLink.get('href'))

def download_latest_file(file_path: str):
    pass



if __name__=="__main__":
    main()
