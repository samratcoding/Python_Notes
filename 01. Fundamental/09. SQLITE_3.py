import sqlite3


connection = sqlite3.connect('sqllite_3.db')
c = connection.cursor()

# Create Data Table 
c.execute('''
            CREATE TABLE IF NOT EXISTS Student(
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Name CHAR(150) NOT NULL UNIQUE,
                Student_id INTEGER NOT NULL UNIQUE,
                Address TEXT
            )
            ''')
c.execute('''
            CREATE TABLE IF NOT EXISTS Student(
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Address TEXT DEFAULT 'Input Your Address'
            )
            ''')


# Insert Data Into existing table
# Try and pass for Unique data
try:
    c.execute('''
                    INSERT INTO Student(
                                Name,
                                Student_id,
                                Address
                                )
                    VALUES
                        ('Samrat rg Biswas', 09634, 'Khulna Sa'),
                        ('Samrhcat ', 764, 'Khulna Sa')
             ''')
except:
    pass


# Data Update
c.execute(''' UPDATE Student
              SET
                Name = "Sam"
              WHERE Name = "Samrat"
            ''')
c.execute(''' UPDATE Student
              SET
                Name = "Sam Update",
                Student_id = 10,
                Address = "Khulna"
              WHERE Name = "Sam"
                ''')
c.execute(''' UPDATE Student
              SET
                Name = "Samru"
              WHERE ID == 1
            ''')

# Dlete DB Data
c.execute('''
            DELETE FROM Student WHERE Student_id == 2 OR ID == 2
            ''')
c.execute('''
            DELETE FROM Student
            ''')

# Data Query
datas1 = c.execute('''SELECT * FROM Student''').fetchall()
datas2 = c.execute('''SELECT Name, Address FROM Student''').fetchall()
datas3 = c.execute('''SELECT * FROM Student WHERE Name="Samrat"''').fetchall()
datas4 = c.execute('''SELECT * FROM Student WHERE Name="Samrat" AND Student_id=3''').fetchall()
single_data = c.execute('''SELECT Name FROM Student WHERE ID=1''').fetchone()[0]

for data in datas1:
    print(data)

connection.commit()
connection.close()