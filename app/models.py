# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
#     DROP DATABASE IF EXISTS employees;
#     CREATE DATABASE IF NOT EXISTS employees;
#     USE employees;

# SELECT 'CREATING DATABASE STRUCTURE' as 'INFO';

# DROP TABLE IF EXISTS dept_emp,
#                      dept_manager,
#                      titles,
#                      salaries, 
#                      employees, 
#                      departments;

# /*!50503 set default_storage_engine = InnoDB */;
# /*!50503 select CONCAT('storage engine: ', @@default_storage_engine) as INFO */;

# CREATE TABLE employees (
#     emp_no      INT             NOT NULL,
#     birth_date  DATE            NOT NULL,
#     first_name  VARCHAR(14)     NOT NULL,
#     last_name   VARCHAR(16)     NOT NULL,
#     gender      ENUM ('M','F')  NOT NULL,    
#     hire_date   DATE            NOT NULL,
#     PRIMARY KEY (emp_no)
# );

# CREATE TABLE departments (
#     dept_no     CHAR(4)         NOT NULL,
#     dept_name   VARCHAR(40)     NOT NULL,
#     PRIMARY KEY (dept_no),
#     UNIQUE  KEY (dept_name)
# );

# CREATE TABLE dept_manager (
#    emp_no       INT             NOT NULL,
#    dept_no      CHAR(4)         NOT NULL,
#    from_date    DATE            NOT NULL,
#    to_date      DATE            NOT NULL,
#    FOREIGN KEY (emp_no)  REFERENCES employees (emp_no)    ON DELETE CASCADE,
#    FOREIGN KEY (dept_no) REFERENCES departments (dept_no) ON DELETE CASCADE,
#    PRIMARY KEY (emp_no,dept_no)
# ); 

# CREATE TABLE dept_emp (
#     emp_no      INT             NOT NULL,
#     dept_no     CHAR(4)         NOT NULL,
#     from_date   DATE            NOT NULL,
#     to_date     DATE            NOT NULL,
#     FOREIGN KEY (emp_no)  REFERENCES employees   (emp_no)  ON DELETE CASCADE,
#     FOREIGN KEY (dept_no) REFERENCES departments (dept_no) ON DELETE CASCADE,
#     PRIMARY KEY (emp_no,dept_no)
# );

# CREATE TABLE titles (
#     emp_no      INT             NOT NULL,
#     title       VARCHAR(50)     NOT NULL,
#     from_date   DATE            NOT NULL,
#     to_date     DATE,
#     FOREIGN KEY (emp_no) REFERENCES employees (emp_no) ON DELETE CASCADE,
#     PRIMARY KEY (emp_no,title, from_date)
# ) 
# ; 

# CREATE TABLE salaries (
#     emp_no      INT             NOT NULL,
#     salary      INT             NOT NULL,
#     from_date   DATE            NOT NULL,
#     to_date     DATE            NOT NULL,
#     FOREIGN KEY (emp_no) REFERENCES employees (emp_no) ON DELETE CASCADE,
#     PRIMARY KEY (emp_no, from_date)
# ) 
# ; 

# CREATE OR REPLACE VIEW dept_emp_latest_date AS
#     SELECT emp_no, MAX(from_date) AS from_date, MAX(to_date) AS to_date
#     FROM dept_emp
#     GROUP BY emp_no;

# # shows only the current department for each employee
# CREATE OR REPLACE VIEW current_dept_emp AS
#     SELECT l.emp_no, dept_no, l.from_date, l.to_date
#     FROM dept_emp d
#         INNER JOIN dept_emp_latest_date l
#         ON d.emp_no=l.emp_no AND d.from_date=l.from_date AND l.to_date = d.to_date;

# flush /*!50503 binary */ logs;

# SELECT 'LOADING departments' as 'INFO';
# source load_departments.dump ;
# SELECT 'LOADING employees' as 'INFO';
# source load_employees.dump ;
# SELECT 'LOADING dept_emp' as 'INFO';
# source load_dept_emp.dump ;
# SELECT 'LOADING dept_manager' as 'INFO';
# source load_dept_manager.dump ;
# SELECT 'LOADING titles' as 'INFO';
# source load_titles.dump ;
# SELECT 'LOADING salaries' as 'INFO';
# source load_salaries1.dump ;
# source load_salaries2.dump ;
# source load_salaries3.dump ;

# source show_elapsed.sql ;