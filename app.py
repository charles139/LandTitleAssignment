from flask import Flask , render_template , flash , redirect , url_for , session , request , logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps

import urllib.request
from xml.etree import ElementTree
import json

app = Flask(__name__)

#CONFIG MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'landtitle_addressbook'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#INITIALIZE MySQL
mysql = MySQL(app)

#Register form class
class AddressForm(Form):
    name = StringField('Name' , [validators.Length(min=1 , max=50)])
    address = StringField('Street Address', [validators.Length(min=4 , max=75)])
    city = StringField('City' , [validators.Length(min=2 , max=50)])
    state = StringField('State' , [validators.Length(min=2 , max=50)])
    zip_code = StringField('Zip' , [validators.Length(min=5 , max=5)])

#Index
@app.route('/')
def index():
    return render_template('index.html')

#View All Addresses
@app.route('/view-all')
def view_all():
    #CREATE CURSOR
    cur = mysql.connection.cursor()

    ##GET articles
    result = cur.execute("SELECT * FROM addresses")

    addresses = cur.fetchall()

    if result > 0:
        return render_template('view-all.html' , addresses = addresses)
    else:
        msg = 'No Artcles Found.'
        return render_template('view-all.html' , msg = msg)
    #CLose connection
    cur.close()

#Add New Address
@app.route('/add-address' , methods = ['GET' , 'POST'])
def add_address():
    form = AddressForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        address = form.address.data
        city = form.city.data
        state = form.state.data
        zip_code = form.zip_code.data

        #Create cursor
        cur = mysql.connection.cursor()

        #EXCECUTE
        cur.execute("INSERT INTO addresses (name , address , city , state , zip_code) VALUES(%s , %s , %s , %s , %s)" , (name , address , city , state , zip_code))

        #commit
        mysql.connection.commit()

        #Close query
        cur.close()

        flash('Address Added' , 'success')

        return redirect(url_for('view_all'))

    return render_template('add-address.html' , form = form)

#Edit Address
@app.route('/edit-address/<string:id>' , methods = ['GET' , 'POST'])
def edit_address(id):
    #CREATE cursor
    cur = mysql.connection.cursor()

    #GET Address by id
    result = cur.execute("SELECT * FROM addresses WHERE id = %s" , [id])

    address = cur.fetchone()

    #Get Form
    form = AddressForm(request.form)

    #Populate address form FIELDS
    form.name.data = address['name']
    form.address.data = address['address']
    form.city.data = address['city']
    form.state.data = address['state']
    form.zip_code.data = address['zip_code']

    if request.method == 'POST' and form.validate():
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']

        #Create cursor
        cur = mysql.connection.cursor()

        #EXCECUTE
        cur.execute("UPDATE addresses SET name = %s , address = %s , city = %s , state = %s , zip_code = %s WHERE id = %s", (name , address , city , state , zip_code , id))

        #commit
        mysql.connection.commit()

        #Close query
        cur.close()

        flash('Address Updated' , 'success')

        return redirect(url_for('view_all'))

    return render_template('edit-address.html' , form = form)

#DELETE Address
@app.route('/delete-address/<string:id>' , methods = ['POST'])
def delete_address(id):
    #CREATE cursor
    cur = mysql.connection.cursor()

    #execute
    cur.execute("DELETE FROM addresses WHERE id = %s" , [id])

    #commit
    mysql.connection.commit()

    #Close query
    cur.close()

    flash('Address Deleted' , 'success')

    return redirect(url_for('view_all'))

if __name__ == '__main__':
    app.secret_key = 'secret139'
    app.run(debug=True)
