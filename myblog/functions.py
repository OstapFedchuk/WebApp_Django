import string
import random
import re
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.template.loader import get_template
from django.template import Context
import bcrypt
from .models import User, Contact

#funzione che controlla se la password ha raggiunto i requisiti minimi per essere sicuri
def requirements_pass(NewPassword):

    length_error = len(NewPassword) < 8
    num_error = re.search(r"\d", NewPassword) is None
    uppercase_error = re.search(r"[A-Z]", NewPassword) is None
    lowercase_error = re.search(r"[a-z]", NewPassword) is None
    symbol_error = re.search(r"\W", NewPassword) is None

    password_ok = not ( length_error or num_error or uppercase_error or lowercase_error or symbol_error )
    
    if password_ok:
        return True
    else:
        return False    

#funzione che serve nel caso di eventuali cambiamenti dei dati va ad aggiornare lo specifico campo
def update_email(row,form,username,mysql):
    error_exist = False

    cur = mysql.get_db().cursor()
        
    if not check_email_exist(form['FormEmail'],mysql):
        if form['FormEmail'] != row[0][1]:
            cur.execute("UPDATE myblog_user SET email=%s WHERE username=%s", (form['FormEmail'],username))
    else:
        error_exist = True
        return error_exist
    
    cur.close()
    return error_exist
    
#OTHER FUNCTION
def update_other_info(row,form,username,mysql):
        cur = mysql.get_db().cursor()

        if form['fullname'] != row[0][2]:
            cur.execute("UPDATE myblog_user SET fullname=%s WHERE username=%s", (form['fullname'],username))
        if form['age'] != row[0][3]:
            cur.execute("UPDATE myblog_user SET age=%s WHERE username=%s", (form['age'],username))
        if form['gender'] != row[0][4]:
            cur.execute("UPDATE myblog_user SET gender=%s WHERE username=%s", (form['gender'],username))
    
        cur.close()
 
    
#password generator for recovery password
def password_generator():
    recovery_psw = ""
    string.letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890\|!"£$%&/()=?*[]@#§-_:.;,'
    
    for x in range(10):
        recovery_psw += random.choice(string.letters)
    
    return recovery_psw

#funzione che serve per settare nel Db la recovery_psw
def insert_rec_psw(User,password,mysql):
    cur = mysql.get_db().cursor()
    cur.execute("UPDATE myblog_user SET password=%s WHERE username=%s OR email=%s", (password,User,User))
    cur.close()

#funzione che va a recuperare la password heshed dal DB
def retrieve_password(User,mysql):
    cur = mysql.get_db().cursor()
    #inserendo il username dell'utente andiamo a recuperare la passsword dal DB
    cur.execute("SELECT password FROM myblog_user WHERE username=%s OR email=%s", (User,User))
    
    result = cur.fetchone()
    return result[0]   

#ritorno tutti i dati dell'utente
def retrieve_all(username,mysql):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM myblog_user WHERE username=%s", (username,))  

    result = cur.fetchall()
    return result

#funzione ch emi ritorna l mail dal DB
def retrieve_email(username,mysql):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT email FROM myblog_user WHERE username=%s", (username,))  

    result = cur.fetchone()
    return result

#funzione che recupera il username basandosi sull'email
def retrieve_user(User,mysql):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT username FROM myblog_user WHERE username=%s OR email=%s", (User,User))

    result = cur.fetchone()
    return result[0]

#funzione che memorizza il username e password nel database
def register_user_to_db(username,email,fullname,age,gender,password,mysql):
    cur = mysql.get_db().cursor()
    cur.execute("INSERT INTO myblog_user (username,email,fullname,age,gender,password) VALUES (%s,%s,%s,%s,%s,%s)", (username,email,fullname,age,gender,password))
    cur.close()

#funzione che serve per salvare i dati del client del contact.html form
def create_message(name,email,subject,message,mysql):
    cur = mysql.get_db().cursor()
    cur.execute("INSERT INTO messages (name,email,subject,message) VALUES (%s,%s,%s,%s)", (name,email,subject,message))
    cur.close()

#funzione che andrà a controllare solo il username
def check_user_exist(username,mysql):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT username FROM myblog_user WHERE username=%s", (username,))

    result = cur.fetchone()
    if result:
        return True
    else: 
        return False
    
#funzione che andrà a controllare solo il username
def check_email_exist(email,mysql):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT email FROM myblog_user WHERE email=%s", (email,))

    result = cur.fetchone()
    if result:
        return True
    else: 
        return False