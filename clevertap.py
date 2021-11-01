import pandas as pd
import requests
from flask import Flask, render_template, request


def JSONify(data):
    events = []
    user = []
    for i in range(len(data)):
        temp = {}
        for j in range(4):
            column = list(data.keys())[j]
            try:
                temp[column] = int(data.iloc[i][column])
            except:
                temp[column] = str(data.iloc[i][column])
        temp1 = {}
        for j in range(5, 18):
            column = list(data.keys())[j]
            try:
                temp1[column] = int(data.iloc[i][column])
            except:
                temp1[column] = str(data.iloc[i][column])
        temp['evtData'] = temp1
        events.append(temp)

        temps = {}

        column = data.keys()[0]

        try:
            temps[column] = int(data.iloc[i][column])
        except:
            temps[column] = str(data.iloc[i][column])
        column = data.keys()[1]

        try:
            temps[column] = int(data.iloc[i][column])
        except:
            temps[column] = str(data.iloc[i][column])
        column = data.keys()[18]
        try:
            temps['type'] = int(data.iloc[i][column])
        except:
            temps['type'] = str(data.iloc[i][column])

        temp1 = {}
        for j in range(19, len(data.keys())):
            column = list(data.keys())[j]
            try:
                temp1[column] = int(data.iloc[i][column])
            except:
                temp1[column] = str(data.iloc[i][column])
        temps['profileData'] = temp1
        events.append(temp)
        user.append(temps)

    events = {'d': events}
    user = {'d': user}

    headers = {
        'X-CleverTap-Account-Id': '8WR-899-KR6Z',
        'X-CleverTap-Passcode': 'SCY-KUV-GWUL',
        'Content-Type': 'application/json; charset=utf-8',
    }

    data = f'''{user}'''
    response1 = requests.post(
        'https://api.clevertap.com/1/upload', headers=headers, data=data)

    print(response1.json())
    data = f'''{events}'''
    response2 = requests.post(
        'https://api.clevertap.com/1/upload', headers=headers, data=data)
    print(response2.json())

    if response1.json()['status'] == response2.json()['status'] == 'success':
        return 'success'
    else:
        return 'fail'


app = Flask(__name__, template_folder='templates')


@app.route('/')
def upload_files():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        data = pd.read_csv(f)
    data.columns = ['identity', 'ts', 'type', 'evtName', 'evtData', 'slotDate', 'teacherName', 'category', 'feedbackForm', 'learningMaterial', 'courseTitle', 'page',
                    'platform', 'source', 'medium', 'utm_ID', 'lessonNumber', 'courseUrl', 'type.1', 'profileData', 'customerType', 'parentName', 'childName', 'childBirthdate']

    return {JSONify(data)}


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8080)
