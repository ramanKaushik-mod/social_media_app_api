
from constants import MESSAGES, LIKES


def trycatch(function, *args):
    try:
        return function(*args)
    except Exception as e:
        return formatApiResponse(
            status='bad-request',
            msg=f'{e}, {e.__class__}'
        )


def executeSQL(cursor, query):
    return cursor.execute(query)


def addFieldsToMESSAGES(message):
    return f'''INSERT INTO {MESSAGES} (message, likers) VALUES ( '{str(message)}', '{{}}' )'''


def addFieldsToLIKES():
    return f'''INSERT INTO {LIKES} DEFAULT VALUES;'''


def updateLikersInMessages(uid: int, msg_id: int, function: str):
    return f'''UPDATE {MESSAGES} SET likers = {function}(likers, {uid}) WHERE msg_id = {msg_id}'''


def isMessageExist(msg_id):
    return f'''SELECT COUNT(*) FROM {MESSAGES} WHERE msg_id = {msg_id}'''


def isLikerExist(uid: int, msg_id: int):
    return f'''SELECT COUNT(*) FROM {MESSAGES} WHERE msg_id = {msg_id} AND {uid} = ANY( likers )'''


def formatApiResponse(status='OK', msg='ok', data={}):
    return {
        'status': status,
        'message': msg,
        'response': data
    }


def tupleToDict(dataSet):
    return {
        "msg_id": dataSet[0],
        "message": dataSet[1],
        "total_likes": dataSet[2]
    }
