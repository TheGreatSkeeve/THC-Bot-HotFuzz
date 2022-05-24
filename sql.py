import sqlite3
from pathlib import Path

dbname = "hotfuzz.db"
dbfolder = "db/"

Path(dbfolder).mkdir(parents=True, exist_ok=True)

# SQL stuff
def sqlite_connect():
    global conn
    conn = sqlite3.connect(dbfolder + dbname, check_same_thread=False)
    conn.row_factory = lambda cursor, row: row[0]

def init_sqlite():
    conn = sqlite3.connect(dbfolder + dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE swearbox (username text, total float )''')
    c.execute('''CREATE TABLE comments (id text)''')


def getUserList():
    sqlite_connect()
    c = conn.cursor()
    c.execute("""SELECT username FROM swearbox""")
    result = c.fetchall()
    return result

def getCharges(username):
    sqlite_connect()
    c = conn.cursor()
    q = [(username)]
    c.execute("""SELECT total FROM swearbox WHERE username=?""",q)
    result = c.fetchall()
    return result[0]

def writeCharges(username,total):
    userList = getUserList()
    if username in userList:
        currentCount = getCharges(username)
        newCount = currentCount + total
        command = '''UPDATE swearbox SET total=? WHERE username=?'''
        q = [(newCount), (username)]
    else:
        command = '''INSERT INTO swearbox('username','total') VALUES(?,?)'''
        q = [(username), (total)]
    sqlite_connect()
    c = conn.cursor()
    c.execute(command, q)
    conn.commit()
    conn.close()

def getComments():
    sqlite_connect()
    c = conn.cursor()
    c.execute("""SELECT id FROM comments""")
    result = c.fetchall()
    return result

def writeComment(id):
    sqlite_connect()
    c = conn.cursor()
    q = [(id)]
    c.execute('''INSERT INTO comments('id') VALUES(?)''', q)
    conn.commit()
    conn.close()


try:
    init_sqlite()
except:
    pass
