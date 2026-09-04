import psycopg2

connection = psycopg2.connect(host='localhost' ,
                              dbname='skills_tracker',
                              user ='postgres',
                              password='mary*Far8',
                              port=5432) 

cursor = connection.cursor()
