import psycopg
from dotenv import load_dotenv
import os
import pandas as pd


members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}

# https://docs.streamlit.io/develop/concepts/connections/secrets-management
load_dotenv()

db_name = os.getenv("DB_NAME")

DB_CONFIG = {
    "user": os.getenv("DB_USERNAME"),
    "dbname": db_name,
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def get_connection():
    return psycopg.connect(**DB_CONFIG)


def insert_menu(menu_name, member_id, dt):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO lunch_menu (menu_name, member_id, dt) VALUES (%s, %s, %s);",
            (menu_name, member_id, dt)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Exception:{e}")
        return False

def select_table():
    query = """
    SELECT
        l.menu_name,
        m.name,
        l.dt
    FROM member m
    INNER JOIN lunch_menu l
    on l.member_id = m.id

    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(rows, columns=['menu_name','name','dt'])
    return df

def select_members_without_lunch():
    query = """
    SELECT
        m.id,
        m.name,
        lm.menu_name,
        lm.dt,
        CURRENT_DATE AT TIME ZONE 'Asia/Seoul' AS today_timestamp,
        DATE(CURRENT_DATE AT TIME ZONE 'Asia/Seoul') AS today_date
    FROM member m
    LEFT JOIN lunch_menu lm
    ON m.id = lm.member_id
    AND lm.dt = DATE(CURRENT_DATE AT TIME ZONE 'Asia/Seoul')
    -- WHERE lm.menu_name IS null
    """

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    selected_columns = []
    for col in cursor.description:
        selected_columns.append(col.name)
    cursor.close()
    conn.close()

    df = pd.DataFrame(rows, columns=selected_columns)
    return df
