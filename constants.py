
# DATABASES
DATABASE = 'social_media_app_db'

# TABLES
MESSAGES = 'messages'
USERS = 'users'
LIKES = 'likes'

# literals
MESSAGE = 'message'
OK_MSG = 'OK'


# SQL QUERIES

CREATE_MESSAGE_TABLE = f'''
    DROP TABLE IF EXISTS {MESSAGES};
    CREATE TABLE {MESSAGES}(
        MSG_ID SERIAL PRIMARY KEY,
        MESSAGE VARCHAR(500) NOT NULL,
        LIKERS INT[]
    );'''

CREATE_LIKES_TABLE = f'''
    DROP TABLE IF EXISTS {LIKES};
    CREATE TABLE {LIKES}(
        MSG_ID SERIAL PRIMARY KEY,
        LIKES INT DEFAULT 0
    );'''

GET_JOIN_OF_MESSAGES_AND_LIKES = f'''
    SELECT {MESSAGES}.msg_id, {MESSAGE}, {LIKES} from {MESSAGES} Inner JOIN {LIKES} on {MESSAGES}.msg_id = {LIKES}.msg_id ORDER BY {MESSAGES}.msg_id DESC;
'''

# TRIGGER FOR LIKES TABLE
CREATE_TRIGGER = f'''
DROP TRIGGER IF EXISTS trigger_likes ON {MESSAGES};
CREATE TRIGGER trigger_likes
    AFTER UPDATE
    ON {MESSAGES}
    FOR EACH ROW
    EXECUTE FUNCTION trigger_likes();'''

# TRIGGER FUNCTION FOR LIKES TABLE
CREATE_TRIGGER_FUNCTION = '''
    CREATE OR REPLACE FUNCTION trigger_likes()
    RETURNS TRIGGER LANGUAGE PLPGSQL AS $likes$
        BEGIN
            IF (TG_OP = 'UPDATE') THEN
                IF (array_length(OLD.likers, 1) is NULL) THEN
                    UPDATE likes SET likes = 1 WHERE msg_id = NEW.msg_id;
                END IF; 
                IF (array_length(NEW.likers, 1) is NULL) THEN
                    UPDATE likes SET likes = 0 WHERE msg_id = NEW.msg_id;
                END IF;                 
                IF (array_length(NEW.likers, 1) > array_length(OLD.likers, 1)) THEN
                    UPDATE likes SET likes = likes + 1 WHERE msg_id = NEW.msg_id;
                END IF;
                IF (array_length(NEW.likers, 1) < array_length(OLD.likers, 1)) THEN
                    UPDATE likes SET likes=likes - 1 WHERE msg_id = NEW.msg_id;
                END IF;
            END IF;
            RETURN NULL;
        END;
    $likes$;
'''
