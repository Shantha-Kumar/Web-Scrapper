import requests
import selectorlib
from mail import send_mail
import time

URL = "http://programmer100.pythonanywhere.com/tours/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape_web(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    extracted_data = extractor.extract(source)['tours']
    return extracted_data


def store(data):
    with open('data.txt', 'a') as file:
        return file.write(data + '\n')

def read_data():
    with open('data.txt', 'r') as file:
        return file.read()


if __name__ == "__main__":
    while True:
        scraped = scrape_web(URL)
        data = extract(scraped)
        content = read_data()

        if data != "No upcoming tours":
            if data not in content:
                store(data)
                # To send ith subjwect check portfolio project
                send_mail(data)
        time.sleep(5)

#python anywhre server streamlit server to free host