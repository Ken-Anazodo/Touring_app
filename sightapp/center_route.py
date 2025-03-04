import os,secrets

from flask import render_template,request,redirect,flash,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash

from sightapp import app
from sightapp.models import db,State,Lga,Resort
from sightapp.myforms import ProfileForm


## creating a function to get user details using their session id
def get_resort_byid(id):
    data = Resort.query.get(id)
    return data #none or an object <Resort>



"""displaying the resort data on the individual pages"""
@app.route("/center/<int:id>/")
def get_resort_page(id):
    ## getting the resort data
    data = Resort.query.get_or_404(id)
    resort_id = session.get('resort_id')
    if resort_id:
        resortdeets = get_resort_byid(resort_id)
    else:
        resortdeets = None

    return render_template("center_details.html",resort_deets=resortdeets,data=data)






"""this route checks if the email a new user is about to input is taken or avaliable"""
@app.route('/center/check_email/')
def check_email():
    email = request.args.get('email')
    status = 'Email is avaliable' #email is avaliable
    data = db.session.query(Resort).filter(Resort.email == email).first()
    if data:
        status = 'Email has been taken' #email is taken
    return status



"""this is the route that renders our resort registrtation page"""
@app.route('/center/register/',methods=['GET','POST'])
def center_register():
    if request.method == 'GET':
        states = db.session.query(State).all()
        return render_template('user/register_center.html', states=states)
    else:
        center = request.form.get('center')
        phone = request.form.get('phone')
        email = request.form.get('email')
        pass1 = request.form.get('pass1')
        pass2 = request.form.get('pass2')
        state = request.form.get('state')
        lga = request.form.get('lga')

        ## vaidate email, name & password
        if email == "" or pass1 == "" or center == "":
            flash('Your Email, Passowrd or Center Name can not be blank','error')
            return redirect(url_for('center_register'))
        elif pass1 != pass2:
            flash("The two passwords must match",'error')
            return redirect(url_for('center_register'))
        else:
            #insert into db and redirect to login page
            hashed = generate_password_hash(pass1)
            r = Resort(name=center,email=email,password=hashed,phone=phone,lga_id=lga,state_id=state)
            try:
                db.session.add(r)
                db.session.commit()
                resort_id = r.id
                ## saving the id into session
                session['resort_id'] = resort_id
                flash('Welcome, an account has been created for you')
                return redirect('/center/dashboard/') 
            except:
                flash('The email is already in use , choose another one')
                return redirect(url_for('center_register'))

 
 
            

"""this route uses ajax to change the lga based on the stateid"""
@app.route('/center/get_lga/')
def get_lga():
    stateid = request.args.get('id')
    data = db.session.query(Lga).filter(Lga.state_id == stateid).all()

    opt = ''
    for d in data:
        lganame = d.name
        lgaid = d.id
        opt = opt + f"<option value='{lgaid}'>{lganame}</option>"

    return opt




"""this route checks if the user is logged in and redirects them to the dashboard page"""
"""user cannot visit the page unless they are logged in"""
@app.route('/center/dashboard/')
def center_dashboard():
    resorts_id = session.get('resort_id')
    if resorts_id:
        resortdeets = get_resort_byid(resorts_id)
        return render_template('user/center_dashboard.html', resort_deets=resortdeets)
    else: #this means session is None
        flash('You need to login to access to this page','error')
        return redirect('/login')




"""this route is for logging out and redirects the user to the login page"""
@app.route('/center/logout')
def center_logout():
    if session.get('resort_id') != None:
        session.pop('resort_id')
    flash('You are now logged out','success')
    return redirect('/login/')





"""the login page"""
@app.route('/login/')
def user_login():
    """this allows those that are logged in and those that are not logged in to visit the login page"""
    resort_id = session.get('resort_id')
    if resort_id:
        resortdeets = get_resort_byid(resort_id)
    else:
        resortdeets = None
    return render_template('login.html', resort_deets=resortdeets)





@app.route('/submit/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')
        usertype = request.form.get('usertype')

        if usertype == '1' : ##tourist
            return 'We will handle tourist login here later'
        elif usertype == '2' :
            resort = db.session.query(Resort).filter(Resort.email == email).first()
            if resort :
                hashed_password = resort.password
                check = check_password_hash(hashed_password,password)
                if check == True:
                    ## save details in session and redirect to dashboard
                    session['resort_id'] = resort.id
                    return redirect('/center/dashboard/')
                else:
                    flash('Incorrect Password','error')
                    return redirect('/login/')
               
            else:
                flash('Email is invalid','error')
                return redirect('/login/')
        else:
            flash('Please choose a usertype' , 'error')
            return redirect('/login/')
           
    else:
        return redirect('/login/')
  
  
  
  
    
"""we can update the tourist center profile in this route (updating data in rosort table)"""
@app.route('/center/profile/', methods=['GET','POST'])
def center_profile():
    resorts_id = session.get('resort_id')
    pform = ProfileForm()
    if resorts_id: #user is logged in

        if request.method == 'GET':
            resortdeets = get_resort_byid(resorts_id)
            return render_template('user/center_profile.html', resort_deets=resortdeets, pform=pform)
        else: ## means they are submitting form by post
            if pform.validate_on_submit(): ## validate form data, retrive data and update details in db
                price = pform.price.data
                description = pform.description.data
                name = pform.name.data
                phone = pform.phone.data
                avaliable = pform.available.data
                cover = request.files.get('cover')
                
                ## getting the filename and getting the extension
                original_filename = cover.filename
                profile = db.session.query(Resort).get(resorts_id)

                ## users can update other details wthout uploading a new file
                if original_filename != '':
                    ext = os.path.splitext(original_filename) ## splitting the file on the extension
                    extension = ext[-1]

                    ## generate new name
                    newfilename = secrets.token_hex(10)
                    cover.save("sightapp/static/uploads/"+newfilename+extension)

                    profile.cover_picture = newfilename+extension


                ## creating an object and putting it into the database
                
                profile.name = name
                profile.phone = phone
                profile.description = description
                profile.avaliable = avaliable
                profile.price = price

                db.session.commit()

                ## upload file using flask form
                flash('File successful updated')
                return redirect (url_for('center_profile'))
            else:
                resortdeets = get_resort_byid(resorts_id)
                return render_template('user/center_profile.html', resort_deets=resortdeets, pform=pform)


    else: #this means session is None
        flash('You need to login to access to this page','error')
        return redirect('/login')
    