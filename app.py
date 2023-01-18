from constants import DATABASE
from db import init
from flask import Flask, request
from handlers import createMessageHandler, createLikesHandler, getMessageHandler
from utility import trycatch, formatApiResponse
app = Flask(__name__)

# initializing database
init(DATABASE)


@app.route("/message", methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        if request.data:
            data = request.get_json()
            return trycatch(createMessageHandler, data)
        else:
            return 'required : [ uid:int, message:str ]'
    elif request.method == 'GET':
        return trycatch(getMessageHandler)
    return formatApiResponse()


@app.route("/like", methods=['POST'])
def like():
    if request.data:
        data = request.get_json()
        return trycatch(createLikesHandler, data)
    else:
        return 'required : [ uid:int, msg_id:int ]'


if __name__ == '__main__':
    app.run(debug=True)
