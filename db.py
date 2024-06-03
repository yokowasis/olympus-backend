import psycopg2
from supabase import create_client, Client

# supabase cred
url: str = "https://gjhlzmuqjhmxmlmqlxgr.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdqaGx6bXVxamhteG1sbXFseGdyIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTk3ODUzMzMsImV4cCI6MTk3NTM2MTMzM30.lFc0VduU5OufjIHJr3TCbvSQqvYgywVXnZOSnOqaS8Q"
supabase: Client = create_client(url, key)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="bimasoft_sdgs",
    user="bimasoft_sdgs",
    password="bimasoft_sdgs",
    host="localhost",
    port=5432
)
cur = conn.cursor()


def abortQuery():
    conn.rollback()


def execQuery(sql, data):
    try:
        cur.execute(sql, data)
        conn.commit()
    except Exception:
        conn.rollback()


def getQuery(sql, data):
    try:
        cur.execute(sql, data)
        return cur.fetchall()
    except Exception:
        conn.rollback()
        return []


def supabaseSelect(table):
    response = supabase.table(table).select("*").execute()
    data = response.data
    return data
