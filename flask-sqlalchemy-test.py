from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

#db = SQLAlchemy(app)

@app.route('/')
def test():
    #results = db.session.query(avenue_eq).all()

    #listResults = list()
    #for r in results:
    #    print(listResults.append(r.Year2018))

    #return str(listResults)
    
    con = sqlite3.connect('test.db')
    print('Database opened successfully.')

    cur = con.cursor()
    cur.execute("select * from Avenue_eq")
   
    rows = cur.fetchall()

    return render_template('_dbTestTemplate.html', rows = rows)

if __name__ == '__main__':
    app.run(debug=True)