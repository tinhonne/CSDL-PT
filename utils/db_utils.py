import sqlite3
import os

DB_PATH = 'database/animalsounds.db'
print("DB_PATH absolute:", os.path.abspath(DB_PATH))

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            zcr REAL, rms REAL, centroid REAL, bandwidth REAL, rolloff REAL,
            mfcc1 REAL, mfcc2 REAL, mfcc3 REAL, mfcc4 REAL, mfcc5 REAL,
            mfcc6 REAL, mfcc7 REAL, mfcc8 REAL, mfcc9 REAL, mfcc10 REAL,
            mfcc11 REAL, mfcc12 REAL, mfcc13 REAL, mfcc14 REAL, mfcc15 REAL,
            mfcc16 REAL, mfcc17 REAL, mfcc18 REAL, mfcc19 REAL, mfcc20 REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_features(filename, features):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO features (
            filename, zcr, rms, centroid, bandwidth, rolloff,
            mfcc1, mfcc2, mfcc3, mfcc4, mfcc5,
            mfcc6, mfcc7, mfcc8, mfcc9, mfcc10,
            mfcc11, mfcc12, mfcc13, mfcc14, mfcc15,
            mfcc16, mfcc17, mfcc18, mfcc19, mfcc20
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (filename, *features))
    conn.commit()
    conn.close()
