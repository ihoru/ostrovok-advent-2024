#!/usr/bin/env python

from flask import Flask, request, render_template, redirect
import os


app = Flask("task1_adminadmin",
            template_folder="./templates",
            static_folder="./static/")

correct_password = "babygirl1" # https://github.com/danielmiessler/SecLists/blob/master/Passwords/Leaked-Databases/rockyou-75.txt : 218
correct_login    = "admin"

flag = r'CTF{EXAMPLE}' if 'FLAG' not in os.environ else os.environ['FLAG'] 


@app.route("/")
def index():
    return redirect('/login')

@app.post("/login")
def login_post():
    data_login = request.form['login']
    data_pass  = request.form['pass']

    if data_login == correct_login and data_pass == correct_password:
        return render_template("flag.html", flag=flag), 200
    if data_login == "admin" and data_pass == "admin":
        return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    return render_template("login.html", error="bad"), 200

@app.get("/login")
def login_get():
    return render_template("login.html", error=""), 200

app.run(host="::",
        port=1337, 
        debug=False)
