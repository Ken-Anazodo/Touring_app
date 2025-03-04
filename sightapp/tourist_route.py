import requests
from flask import render_template,request,redirect,flash,session,url_for 

from werkzeug.security import generate_password_hash,check_password_hash

from sightapp import app
from sightapp.models import db,Resort,User

"""this route displays the home page"""
@app.route('/')
def home_page():
    ## using the api of property app and accouting for when their server is down
    try:
        response = requests.get('http://127.0.0.1:3000/api/v1/listall/')
        response_json = response.json()
    except:
        response_json = None

    allresorts = db.session.query(Resort).filter(Resort.status == 'active').all()
    ## this checks if the session is empty and allows us to use it to create a database object and access the data in the home page
    if session.get('resort_id') != None:
        rid = session.get('resort_id')
        resort_deets = db.session.query(Resort).get(rid)
    else:
        resort_deets = None

    return render_template('index.html',resort_deets=resort_deets, allresorts=allresorts, response_json=response_json)


"""tourist sign up page"""
# @app.route('/tourist/register',methods=['GET','POST'])
# def tourist_register():
#     if session.get('resort_id') != None:
#         rid = session.get('resort_id')
#         resort_deets = db.session.query(Resort).get(rid)
#         if request.method == 'GET':
#             return render_template('user/register_tourist.html',resort_deets=resort_deets)
#         else:
#             fname = request.form.get('fname')
#             lname = request.form.get('lname')
#             phone = request.form.get('phone')
#             email = request.form.get('email')
#             pass1 = request.form.get('pass1')
#             pass2 = request.form.get('pass2')

#             ## vaidate email, name & password
#             if email == "" or pass1 == "" or fname == '' or lname == '':
#                 flash('Your Email, Passowrd or Names can not be blank','error')
#                 return redirect(url_for('center_register'))
#             elif pass1 != pass2:
#                 flash("The two passwords must match",'error')
#                 return redirect(url_for('center_register'))
#             else:
#                 #insert into db and redirect to login page
#                 hashed = generate_password_hash(pass1)
#                 r = User(fname=fname,lname=lname,email=email,password=hashed,phone=phone)
#                 try:
#                     db.session.add(r)
#                     db.session.commit()
#                     resort_id = r.id
#                     ## saving the id into session
#                     session['resort_i'] = resort_id
#                     flash('Welcome, an account has been created for you')
#                     return redirect('/center/dashboard/') 
#                 except:
#                     flash('The email is already in use , choose another one')
#                     return redirect(url_for('tourist_register'))
#     else:
#         resort_deets = None

#     return render_template('user/register_tourist.html',resort_deets=resort_deets)