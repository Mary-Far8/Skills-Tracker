import psycopg2

def add_skill_to_db(cursor, connection, name, progress) :
    try:
        cursor.execute('INSERT INTO skills (name, progress) VALUES (%s, %s)', (name, progress))
        connection.commit()
        return True
    except psycopg2.errors.UniqueViolation:
        connection.rollback()
        return False


def get_all_skills(cursor) :
    cursor.execute("SELECT * FROM skills")
    rows = cursor.fetchall()
    return rows 


def update_skills_in_db(connection , cursor , name, new_progress):
    cursor.execute('UPDATE skills SET progress = %s WHERE name = %s', (new_progress, name))
    connection.commit()
    updated = cursor.rowcount > 0
    return updated


def delete_skills_from_db(cursor,connection,name):
    cursor.execute('DELETE FROM skills WHERE name = %s', (name,))
    deleted = cursor.rowcount > 0
    connection.commit()
    return deleted 
