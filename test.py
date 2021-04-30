import requests
import json

url = "http://localhost:4000/tweets/"

json_data = {
    "tags": [{
        "tag": "test1",
        "weight": 1
    },
        {
            "tag": "test2",
            "weight": 1
        }],
    "date": "10/12/2020",
    "author": "Elon Musk",
    "tweet_text": "Test string with the tweet",
    "url": "This be url",
    "tweet_id": "stff",
    "question_id": "ss"
}

json_data['author'] = "Sp,ejtong"

print(json_data["author"])

headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(json_data))

print(response.text)
