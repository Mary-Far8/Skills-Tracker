from fastapi import FastAPI  
import psycopg2
from Skills_Tracker import get_all_skills,add_skill_to_db,delete_skills_from_db,update_skills_in_db 

connection = psycopg2.connect(host="localhost",
                             dbname="skills_tracker",
                             user='postgres',
                             password="mary*Far8",
                             port=5432)

cursor = connection.cursor()
cursor.execute('SELECT VERSION();')

app = FastAPI() 

@app.get("/")
def home():
    return {'message':'Hello from FastAPI'}

@app.get("/skills")
def read_skills():
    rows = get_all_skills(cursor)
    return{"skills":rows} 

@app.post("/skills")
def add_skills(name:str , progress:int):
    success = add_skill_to_db(cursor,connection,name,progress)
    return{'success':success} 

@app.delete("/skills/{name}")
def delete_skills(name:str):
    success = delete_skills_from_db(cursor,connection,name)
    return{'success':success}

@app.put("/skills/{name}")
def update_skills(name:str, new_progress:int):
    success = update_skills_in_db(connection,cursor,name,new_progress)
    return{'success':success}



