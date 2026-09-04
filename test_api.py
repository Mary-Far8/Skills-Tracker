from fastapi.testclient import TestClient 
from api import app 
from Skills_Tracker import delete_skills_from_db,cursor,connection,add_skill_to_db



client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200 
    assert response.json() == {'message':'Hello from FastAPI'}  

def test_read_skills():
    response = client.get("/skills")
    assert response.status_code == 200
    data = response.json()
    assert "skills" in data 
    assert isinstance(data['skills'], list)

def test_add_skills():
    delete_skills_from_db(cursor, connection,'testskills')
    response = client.post("/skills", params={"name":"testskills","progress":"5"})
    assert response.status_code == 200
    assert response.json() == {'success':True} 
    delete_skills_from_db(cursor, connection,'testskills') 

def test_delete_skills():
    add_skill_to_db(cursor, connection, 'testskills', 5)
    response = client.delete("/skills/testskills")
    assert response.status_code == 200
    assert response.json() == {'success': True}

def test_update_skills():
    add_skill_to_db(cursor, connection, 'testskills', 5)
    response = client.put("/skills/testskills", params={"new_progress": 50})
    assert response.status_code == 200
    assert response.json() == {'success': True}
    delete_skills_from_db(cursor, connection, 'testskills')







