import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?,?,?) """
    DB.execute(query, (first_name, last_name, github))

    CONN.commit()
    print "Successfully added student:%s %s" % (first_name, last_name)

def get_project_title(project_title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (project_title,))
    row = DB.fetchone()
    print """\
    Project title: %s
    Description: %s
    Max grade: %d""" % (row[1],row[2],row[3])

def make_new_project(title, description, max_grade):
    query = """ INSERT into Projects (title, description, max_grade) values (?,?,?)"""
    DB.execute(query, (title, description, max_grade))

    CONN.commit()
    print "Successfully added project: %s" % (title)

def get_grade(github, project_title):
    query = """SELECT grade FROM
    Grades JOIN Students ON
    (github = student_github)
    WHERE github = ? AND project_title = ?"""
    DB.execute(query, (student,))
    row = DB.fetchone()

    print """ Successfully added
    Student: %s %s
    Project: %s
    Grade: %s
    """ % (row[0], row[1],row[3],row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project_title":
            get_project_title(*args)
        elif command == "add_project":
            make_new_project(*args)
        elif command == "get_grade":
            get_grade(*args)

    CONN.close()

if __name__ == "__main__":
    main()
