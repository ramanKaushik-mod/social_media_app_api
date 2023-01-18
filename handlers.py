
from db import getDBConnection
from utility import addFieldsToLIKES, addFieldsToMESSAGES, executeSQL, isLikerExist, isMessageExist, updateLikersInMessages, formatApiResponse, tupleToDict

from constants import DATABASE, GET_JOIN_OF_MESSAGES_AND_LIKES


def createMessageHandler(data):
    conn = getDBConnection(DATABASE)
    cursor = conn.cursor()
    if not data['message']:
        raise Exception('payload does not contain the field : [message]')
    if not data['uid']:
        raise Exception('payload does not contain the field : [uid]')
    msg = data['message'].replace("'", r"''")
    requiredSQl = addFieldsToMESSAGES(message=msg)
    executeSQL(cursor, requiredSQl)
    requiredSQl = addFieldsToLIKES()
    executeSQL(cursor, requiredSQl)
    conn.close()
    return formatApiResponse()


def createLikesHandler(data):
    conn = getDBConnection(DATABASE)
    cursor = conn.cursor()
    if not data['uid']:
        raise Exception('payload does not contain the field : [message]')
    if not data['msg_id']:
        raise Exception('payload does not contain the field : [uid]')
    requiredSQl = isMessageExist(msg_id=data['msg_id'])
    executeSQL(cursor=cursor, query=requiredSQl)
    record = cursor.fetchone()
    print(record, "msg")
    if record[0] == 0:
        raise Exception(
            f"""no message exist with this id : [{data['msg_id']}]""")

    requiredSQl = isLikerExist(uid=data['uid'], msg_id=data['msg_id'])
    executeSQL(cursor=cursor, query=requiredSQl)
    record = cursor.fetchone()
    func = 'array_append'
    msg = 'liked'
    if record[0] != 0:
        func = 'array_remove'
        msg = 'disliked'
    requiredSQl = updateLikersInMessages(
        function=func,
        msg_id=data['msg_id'], uid=data['uid']
    )
    executeSQL(cursor, requiredSQl)
    conn.close()
    return formatApiResponse(msg=msg)


def getMessageHandler():
    conn = getDBConnection(DATABASE)
    cursor = conn.cursor()
    requiredSQl = GET_JOIN_OF_MESSAGES_AND_LIKES
    executeSQL(cursor=cursor, query=requiredSQl)
    dataSet = cursor.fetchall()
    data = []
    for record in dataSet:
        data.append(tupleToDict(record))
    return formatApiResponse(data=data)
