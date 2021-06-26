from flask import Flask, config, request
from flask_mongoengine import MongoEngine
import json
import os

app = Flask(__name__)

LOCAL_FILE = "./backend/local.json"
GLOBAL_FILE = "./backend/global.json"

STATUS_OK = {"STATUS": "OK"}
STATUS_ERR = {"STATUS": "ERROR"}


def to_json(meetingName, meetingId, meetingCode, settings):
    return {
        "meetingName": meetingName,
        "meetingId": meetingId,
        "meetingCode": meetingCode,
        "settings": settings
    }


def global_to_json(announcements, faqs, textCommands, queueCommands, wakeWord):
    return {
        "announcements": announcements,
        "faqs": faqs,
        "textCommands": textCommands,
        "queueCommands": queueCommands,
        "wakeWord": wakeWord
    }


@app.put('/api/global')
def add_global_settings():
    record = json.loads(request.data)
    print(record)  #debugging
    with open(GLOBAL_FILE, "r") as f:
        if os.path.getsize(GLOBAL_FILE) != 0:
            data = json.load(f)
        else:
            data = {}
    with open(GLOBAL_FILE, "w") as f:
        data["settings"] = global_to_json(record["announcements"],
                                          record["faqs"],
                                          record["textCommands"],
                                          record["queueCommands"],
                                          record["wakeWord"])
        json.dump(data, f, indent=4, sort_keys=True)
    return (STATUS_OK)


@app.put('/api/local/')
def create_meeting():
    record = json.loads(request.data)
    print(record)  #debugging
    with open(LOCAL_FILE, "r") as f:
        if os.path.getsize(LOCAL_FILE) != 0:
            data = json.load(f)
        else:
            data = {}
    with open(LOCAL_FILE, "w") as f:
        data[record["meetingId"]] = to_json(record["meetingName"],
                                            record["meetingId"],
                                            record["meetingCode"],
                                            record["settings"])
        json.dump(data, f, indent=4, sort_keys=True)
    return (STATUS_OK)


@app.get('/api/local/')
def get_meeting():
    record = json.loads(request.data)
    print(record)  #debugging
    if os.path.getsize(LOCAL_FILE) == 0:
        return (STATUS_ERR)
    with open(LOCAL_FILE, "r") as f:
        data = json.load(f)
    try:
        added = data[record["meetingId"]]
    except KeyError:
        return (STATUS_ERR)
    else:
        added = data[record["meetingId"]]
        return added


@app.delete('/api/local/')
def delete_meeting():
    record = json.loads(request.data)
    print(record)  #debugging
    if os.path.getsize(LOCAL_FILE) == 0:
        return (STATUS_ERR)
    with open(LOCAL_FILE, "r") as f:
        data = json.load(f)
        try:
            deleted = data[record["meetingId"]]
        except KeyError:
            return (STATUS_ERR)
    with open(LOCAL_FILE, "w") as f:
        data.pop(record["meetingId"])
        json.dump(data, f, indent=4, sort_keys=True)
    return (STATUS_OK)


@app.post('/api/local/')
def update_meeting():
    record = json.loads(request.data)
    print(record)  #debugging
    if os.path.getsize(LOCAL_FILE) == 0:
        return (STATUS_ERR)
    with open(LOCAL_FILE, "r") as f:
        data = json.load(f)
    with open(LOCAL_FILE, "w") as f:
        data[record['meetingId']] = record
        json.dump(data, f, indent=4, sort_keys=True)
    return (STATUS_OK)


if __name__ == "__main__":
    app.run()