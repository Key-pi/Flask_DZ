import csv
import requests
import json
from faker import Faker
from flask import Flask
from flask import request


app = Flask(__name__)


@app.route('/requirements/')
def show_req_info():
    with open("requirements.txt", "r") as f:
        req_info = f.readlines()
        text = ''

        for line in req_info:
            text += line

        text = text.replace('\n', '<br>')

        return text


@app.route('/generate-users/')
def fake_users():
    fake = Faker()
    quantity = int(request.args.get('count', 100))
    result_users = "<br>".join([f"{fake.name()} - {fake.email()}" for _ in range(quantity)])
    return result_users


@app.route("/mean/")
def average_values():
    sum_w, sum_h, n = 0, 0, 0
    with open('hw.csv', newline='') as cv:
        text = csv.reader(cv, delimiter=' ', quotechar='|')
        for row in text:
            n += 1
            if n == 1:
                continue
            else:
                row[0] = row[0].replace(',', '')
                row[1] = row[1].replace(',', '')
                row[2] = row[2].replace(',', '')
                row = list(map(float, row))
                sum_h += row[1]
                sum_w += row[2]
    sum_h *= 2.54
    sum_w *= 2.205
    n -= 1
    sum_h /= n
    sum_w /= n
    return f"Средний рост(см) {sum_h}<br>Средний вес(кг) {sum_w} "


@app.route('/space/')
def show_cosmonaut():
    response = requests.get("http://api.open-notify.org/astros.json")
    number = json.loads(response.text)
    return f"{number['number']}"
