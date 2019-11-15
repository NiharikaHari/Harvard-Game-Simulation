from flask import Flask, render_template, request, flash, session, abort, redirect, url_for
import os
import pandas as pd
import numpy as np
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)
#app.config('SECRET_KEY') = ''
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

#db = SQLAlchemy(app)

regnoDirectory = list(np.arange(1740201,1740288))

loginDirectory = {
    1740217: 'shornabho',
    1740236: 'shreya',
    1740219: 'vaibhav',
    1740245: 'gary',
    1740231: 'niharika'
}

@app.route('/signup', methods = ['POST','GET'])
def signup():
    

    if request.method == 'POST':
        regno = int(request.form['regno'])
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if regno in regnoDirectory:
            if regno not in loginDirectory:
                if 'username' in session:
                    session.pop('username',None)
                loginDirectory[regno] = password
                return redirect(url_for('login'))
            else:
                return 'Already a user!'
        else:
            return 'Not authorized to sign up! Sorry!'
    return render_template('signup.html')

@app.route('/', methods = ['GET','POST'])
@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        username = int(request.form['username'])
        password = request.form['password']
        
        if username in loginDirectory:
            if loginDirectory[username] == password:
                session['username'] = request.form['username']
                return redirect(url_for('gamePage'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    else:
        if 'username' in session:
            return redirect(url_for('gamePage'))
        else:
            return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return 'You have been logged out!'

@app.route('/checksession')
def checksession():
    if 'username' in session:
        return 'Status: Logged in'
    else:
        return 'Status: Logged out'


industries = pd.DataFrame({'Industry A':[1,2,3,4],
                          'Industry B':[5,6,7,8],
                          'Industry C':[9,10,11,12]}, index=['Fixed Capital','Working Capital','Fixed Assets','PNL Balance'])

#@app.route('/', methods = ("POST","GET"))
@app.route('/testLayout/', methods = ("POST","GET"))
def test():
    return render_template("main.html", tables = [industries.to_html(classes = ['table','table-striped-balancesheet'],header = "true")], titles = industries.columns.values)


@app.route('/gamePage')
def gamePage():
    if 'username' in session:
        

        con = sqlite3.connect('test.db')
        print('Database opened successfully.')

        # Income Statement

        cur = con.cursor()
        cur.execute("select * from mastersheetIncome")
    
        incomeStatement = cur.fetchall()
        
        # Balance Sheet

        cur = con.cursor()
        cur.execute("select * from mastersheetBalanceSheet")
    
        balanceSheet = cur.fetchall()

        # Ratios
        cur = con.cursor()
        cur.execute("select * from mastersheetRatios")
    
        ratios = cur.fetchall()

        return render_template('gamePage.html', incomeStatement = incomeStatement, balanceSheet = balanceSheet, ratios = ratios)
    return 'You are not logged in!'


if __name__ == '__main__':
    app.run(debug=True)