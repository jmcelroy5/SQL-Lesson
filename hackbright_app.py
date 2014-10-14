import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    try:
        query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
        DB.execute(query, (github,))
        row = DB.fetchone()
        print """\
        Student: %s %s
        Github account: %s"""%(row[0], row[1], row[2])
    except TypeError:
        print "Oops! No student has that github!"
    
def make_new_student(first_name, last_name, github):
        query = """INSERT into Students values (?,?,?) """
        DB.execute(query, (first_name, last_name, github))
        CONN.commit()
        print "Successfully added student:%s %s" % (first_name, last_name)

def get_project_title(project_title): 
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (project_title,))
    row = DB.fetchone()
    print """
    Project title: %s
    Description: %s
    Max grade: %d""" % (row[1],row[2],row[3])

def make_new_project(title, description, max_grade):
    query = """ INSERT into Projects (title, description, max_grade) values (?,?,?)"""
    DB.execute(query, (title, description, max_grade))

    CONN.commit()
    print "Successfully added project: %s" % (title)

def give_grade(student_github, project_title, grade):
    query = """INSERT into Grades (student_github, project_title, grade) values (?,?,?)"""
    DB.execute(query, (student_github, project_title, grade))

    CONN.commit()
    print "Successfully gave %s the grade %s on %r" %(student_github, grade, project_title)

def show_grades(first_name,last_name):
    query = """SELECT DISTINCT Grades.project_title, Grades.grade 
    FROM Students JOIN Grades ON (Students.github=Grades.student_github)
    WHERE Students.first_name = ? AND Students.last_name = ?
    """
    DB.execute(query, (first_name, last_name,))
    row = DB.fetchall()
    for i in range(len(row)):
        print """
        Project: %s
        Grade: %r
        """ % (row[i][0],row[i][1])

def get_grade(last_name, project_title):  
    query = """SELECT Grades.grade, Students.first_name, Students.last_name, Grades.project_title 
    FROM Grades JOIN Students ON (github = student_github)
    WHERE Students.last_name = ? AND Grades.project_title = ?"""
    DB.execute(query, (last_name, project_title,))
    row = DB.fetchone()

    print """ Successfully added
    Student: %s %s
    Project: %s
    Grade: %d
    """ % (row[1],row[2],row[3],row[0]) 

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        # tokens = input_string.split()
        
        try:
            (command, tokens) = input_string.split(None, 1) 
            args = tokens.split(",") # User needs to enter arguments separated by commas
        except IndexError:
            input_string = raw_input("HBA Database> ")
        except ValueError:
            input_string = raw_input("HBA Database> ")

        if command == "student":
            try:
                get_student_by_github(*args)
            except TypeError:
                print "The student command takes exactly one argument: github username"
        elif command == "new_student":
            try:
                make_new_student(*args)
            except TypeError:
                print "The new_student command takes 3 args: first name, last name, github"
        elif command == "project_title":
            try:
                get_project_title(*args)
            except TypeError:
                print "The project_title command takes exactly one argument: project title"
        elif command == "add_project":
            try: 
                make_new_project(*args)
            except TypeError:
                print "The add_project command takes exactly three arguments: project title, description (one word), and max grade."
        elif command == "get_grade":
            try:
                get_grade(*args)
            except TypeError:
                print "The get_grade command takes two arguments: student last name, project title"
        elif command == "give_grade":
            try:
                give_grade(*args)
            except TypeError:
                print "The give_grade command takes exactly three arguments: student's github, project title, grade"
        elif command == "show_grades":
            try:
                show_grades(*args)
            except TypeError:
                print "The show_grades command takes exactly two arguments: first name, last name"
                
    CONN.close()

if __name__ == "__main__":
    main()
