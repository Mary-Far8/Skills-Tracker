import pytest
import sqlite3
import psycopg2
from Skills_Tracker import add_skill_to_db
from Skills_Tracker import delete_skills_from_db
from Skills_Tracker import update_skills_in_db,get_all_skills


@pytest.fixture
def db_connection():
    conn = psycopg2.connect(host= 'Localhost' ,
                            dbname= 'skills_tracker',
                            user= 'postgres',
                            password= 'mary*Far8',
                            port= 5432)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM skills""")
    conn.commit()

    yield cursor, conn

    cursor.execute("""DELETE FROM skills""")
    conn.commit()
    conn.close()


def test_add_skill_to_db(db_connection):
    print(db_connection)          # <-- add this temporarily, just to SEE what it is
    cursor, conn = db_connection
    result = add_skill_to_db(cursor, conn, 'python', 1)
    assert result == True 

def test_delete_skill_to_db(db_connection):
    cursor,conn = db_connection
    add_skill_to_db(cursor, conn, 'python', 1)
    result = delete_skills_from_db(cursor,conn,'python')
    assert result == True

def test_update_skill_to_db(db_connection):
    cursor,conn= db_connection
    add_skill_to_db(cursor, conn, 'python', 1)
    result = update_skills_in_db (conn, cursor ,'python' , 10)
    assert result == True 

def test_refresh_skills_list(db_connection):
    cursor, conn = db_connection
    
    add_skill_to_db(cursor, conn, 'python', 1)
    add_skill_to_db(cursor, conn, 'pytest', 2)
    delete_skills_from_db(cursor, conn, 'pytest')
    rows = get_all_skills(cursor)

    assert len(rows) == 1
    names_and_progress = [(name, progress) for (_, name, progress) in rows]
    assert ('python', 1) in names_and_progress