# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import redirect, render_template, render_template_string, Blueprint
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from app.init_app import app, db
import os 
from datetime import datetime
from app.models import UserProfileForm
import json


# The Home page is accessible to anyone
@app.route('/home')
def home_page():
    return render_template('pages/home_page.html')

@app.route('/')
def home():
    return render_template('pages/home.html')


# The User page is accessible to authenticated users (users that have logged in)
@app.route('/user')
@login_required  # Limits access to authenticated users
def user_page():
    
    
    try: 
        os.makedirs("app/static/upload/"+str(current_user.id),exist_ok=True)
    except: pass 

    return render_template('pages/user_page.html')

@app.route('/login')
def login():
    return render_template('pages/login.html')


# The Admin page is accessible to users with the 'admin' role
@app.route('/admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('pages/admin_page.html')

@app.route('/ajaxcalc',methods=['POST', 'GET'])
@login_required
def ajaxcalc():
    if request.method=='POST':
        data=request.get_json()
        print(data)
        with open('app/static/upload/'+str(current_user.id)+'/tracks'+str(datetime.utcnow())+'.json', 'w') as outfile:
            json.dump(data, outfile)
        return ("ok")
    else:
        return ("error")

@app.route ('/tracks', methods =['POST','GET'])
@login_required
def Track_list():
    tracks = os.listdir('/app/static/upload/'+ str(current_user.id))
    return jsonify(tracks)
    

@app.route('/pages/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, current_user)

    

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('home_page'))

    # Process GET or invalid POST
    return render_template('pages/user_profile_page.html',
                           form=form)


