'''Original code inspired by https://docs.python.org/3/library/sqlite3.html'''

import sqlite3
import pandas as pd
"Used for debugging/testing purposes"

db = sqlite3.connect('donations') 
cursor = db.cursor()

# cursor.execute('''
#         CREATE TABLE IF NOT EXISTS users
#         ([user_id]INTEGER PRIMARY KEY, [user_name] TEXT, [password] TEXT, 
#         [user_score] INTEGER)
#         ''')
    
# cursor.execute('''
#         INSERT INTO users (user_id, user_name, password, user_score)
#         VALUES
#         ("1", 'Rex', 'sharktruck', '20')
#         ''')

# cursor.execute('''
#         INSERT INTO users (user_id, user_name, password, user_score)
#         VALUES
#         ("2", 'Talay', 'sharktruck2', '30')
#         ''')

# cursor.execute('''
#         INSERT INTO users (user_id, user_name, password, user_score)
#         VALUES
#         ("3", 'Danny', 'sharktruck3', '40')
#         ''')

# cursor.execute('''
#         CREATE TABLE IF NOT EXISTS donations
#         ([donation_id]INTEGER PRIMARY KEY, [object] TEXT, [cause] TEXT,  
#         [user_id] INTEGER, [donation_scores] INTEGER, [x] REAL, [y] REAL, 
#         FOREIGN KEY(user_id)
#             REFERENCES users (user_id))
#         ''')

# cursor.execute('''
#         INSERT INTO donations (object, cause, user_id, donation_scores, x, y)
#         VALUES
#         ('kidney', 'help ppl with no kidney', '1', '20', '5', '10')
#         ''')

cursor.execute('''
                SELECT * FROM donations
                ''')

# df=pd.DataFrame(cursor.fetchall(), columns=['user_id', 'user_name', 'password', 'user_score'])

df=pd.DataFrame(cursor.fetchall(), columns=['donation_id', 'object', 'cause', 'user_id', 'donation_scores', 'x', 'y'])

for user_id in df.user_id:
    cursor.execute(f'''
                SELECT * FROM donations WHERE user_id = {user_id}
                ''')
    df2 = pd.DataFrame(cursor.fetchall(), columns=['user_id', 'user_name', 'password', 'user_score'])

# db.commit()
print(df)