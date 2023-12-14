import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime as dt

load_dotenv()

HOST = os.getenv('host')
USER = os.getenv('user')
PW = os.getenv('password')
DB = os.getenv('database')

connPOSTGRES = psycopg2.connect(
    host = HOST,    
    user = USER,
    password = PW,
    database = DB
)


     