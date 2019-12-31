from flask import Flask, render_template, request, flash, session, abort, redirect, url_for
import os
import pandas as pd
import numpy as np
import sqlite3
from passlib.hash import sha256_crypt
from dbConnect import connection
import gc
from datetime import datetime

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
        course = request.form['course']
        email = request.form['email']
        password = sha256_crypt.encrypt(request.form['password'])

        # Check for regno validity
        if regno not in regnoDirectory:
            # flash('Not authorized to sign up! Sorry!')
            return 'Not authorized to sign up! Sorry!'

        c, conn = connection('usersdb')

        c.execute('SELECT * FROM students WHERE regno=%s;',tuple([regno]))
        x = c.fetchall()
        if len(x) > 0:
            # Duplicate username                
            
            #flash("That username is already taken, please choose another")

            return 'You are already a user!<br><br><a href="/login">Log in</a> to your account.'

            #return render_template('signup.html', signupStatus = signupStatus)

        else:
            # Valid username

            # Logout from existing user
            if 'regno' in session:
                session.clear()

            # Insert new user into database
            c.execute('INSERT INTO students(regno,name,course,email,password,date_created) VALUES(%s,%s,%s,%s,%s,%s)',(regno,name,course,email,password, datetime.now()))
            conn.commit()
            
            flash("Thanks for registering!")
            c.close()
            gc.collect()

            # Signup successful
            signupStatus = 'Successfully signed up!'

            # Login to new user
            session['logged_in'] = True
            session['regno'] = regno
            session['name'] = name

            return redirect(url_for('gamePage'))


        
    return render_template('signup.html', signupStatus='')

@app.route('/', methods = ['GET','POST'])
@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        alertPassword = ''
        alertUsername = ''

        #return render_template('gamePage.html')
        try:
            c, conn = connection('usersdb')
            c.execute("SELECT * FROM students WHERE regno = %s", tuple([request.form['username']]))
            data = c.fetchall()

            if len(data) > 0:
                if sha256_crypt.verify(request.form['password'], data[0][4]):
                    session['logged_in'] = True
                    session['regno'] = request.form['username']
                    session['name'] = data[0][1]

                    flash("You are now logged in")
                    return redirect(url_for("gamePage"))

                else:
                    alertPassword = "Invalid password, try again."
                    return render_template("login.html", alertPassword = alertPassword)
            else:
                alertUsername = "Invalid username, try again."
                return render_template("login.html", alertUsername = alertUsername) 
            c.close()
            gc.collect()
            
        except Exception as e:
            #flash(e)
            return (str(e))
    else:
        if 'regno' in session:
            return redirect(url_for('gamePage'))
        else:
            return render_template('login.html', alertPassword = '')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('regno',None)
    return redirect(url_for('login'))

@app.route('/checksession')
def checksession():
    if 'regno' in session:
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
    if 'regno' in session:
        
        # Load gamepage:
        #return render_template('gamePage.html')
        c, conn = connection('mydb')
        
        incomeStatementFields = ('Excise Duty','Material Expenses','Stock In Trade','Employee Cost','Fuel & Electricity')
        balanceSheetFields = ('PPE','Inventory','Trade Receivables','Trade Payables')
        ratiosFields = ('Receivable Days','Inventory Days','Payable Days','EBITDA Margin(%)','Asset Turnover (times)','Return on Assets(%)','Return on Networth (%)')
        # Income Statement
        c.execute("select * from mater_table where Fields = %s or Fields = %s or \
            Fields = %s or Fields = %s or Fields = %s;",incomeStatementFields)
        incomeStatement = c.fetchall()
        
        # Balance Sheet
        c.execute("select * from mater_table where Fields = %s or Fields = %s or \
            Fields = %s or Fields = %s;",balanceSheetFields)  
        balanceSheet = c.fetchall()

        # Ratios
        c.execute("select * from mater_table where Fields = %s or Fields = %s or \
            Fields = %s or Fields = %s or Fields = %s or Fields = %s or Fields = %s;",ratiosFields)
        ratios = c.fetchall()
        
        conn.close()
        gc.collect()

        return render_template('abc.html', name = session['name'], incomeStatement = incomeStatement, balanceSheet = balanceSheet, ratios = ratios)
    
    return redirect(url_for('login'))

@app.route('/tutorial')
def tutorial():
    if 'regno' in session:
        return render_template('tutorial.html')
    return 'You are not logged in!'

@app.route('/faq')
def faq():
    if 'regno' in session:
        return render_template('faq.html')
    return 'You are not logged in!'

if __name__ == '__main__':
    app.run(debug=True)