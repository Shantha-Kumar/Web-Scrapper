import requests
import selectorlib
from mail import send
import time
import sqlite3

connection = sqlite3.connect('data.db')

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
    row = data.split(',')
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read_data(data):
    row = data.split(',')
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                   (band, city, date))  # instead of tuple u can also use row
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    while True:
        scraped = scrape_web(URL)
        data = extract(scraped)

        if data != "No upcoming tours":
            row = read_data(data)
            if not row:
                store(data)
                # To send with subject check portfolio project
                send(data)
                print("Mail sent")
        time.sleep(1)

# python anywhere server streamlit server to free host
