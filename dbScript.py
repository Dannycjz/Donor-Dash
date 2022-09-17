'''Original code inspired by https://docs.python.org/3/library/sqlite3.html'''

import sqlite3
import pandas as pd
"Used for debugging/testing purposes"

db = sqlite3.connect('chess') 
cursor = db.cursor()

# cursor.execute('''
#         CREATE TABLE IF NOT EXISTS users
#         ([LastCall]INTEGER, [Latitude] REAL, [Longtitude] REAL, 
#         [Thumbs] INTEGER, [Tag] TEXT)
#         ''')
    
# cursor.execute('''
#         INSERT INTO users (user_id, user_name, password)
#         VALUES
#         ([CURRENT TIME], '51', '-1', '1', 'tartanhack2022')
#         ''')

cursor.execute('''
                SELECT * FROM users
                ''')

df=pd.DataFrame(cursor.fetchall(), columns=['user_id', 'user_name', 'password'])

#db.commit()
print(df)