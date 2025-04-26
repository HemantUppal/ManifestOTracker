from flask import Flask, render_template, request, redirect, url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_,or_
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required, current_user
from model import db,User,Manifesto, Votes,Complaint,Reports
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()



@app.route('/')

def home():
    return render_template('home.html',user=current_user)

@app.route('/upvote/<int:scheme_id>')
@login_required
def upvote(scheme_id):
    # Check if user already voted on this scheme
    existing_vote = Votes.query.filter_by(user_id=current_user.id, scheme_id=scheme_id).first()

    if existing_vote:
        existing_vote.upvote += 1
    else:
        vote = Votes(user_id=current_user.id, scheme_id=scheme_id, upvote=1, downvote=0)
        db.session.add(vote)

    db.session.commit()
    flash("Your upvote has been recorded!", "success")
    return redirect(request.referrer or url_for('cengov'))

@app.route('/downvote/<int:scheme_id>')
@login_required
def downvote(scheme_id):
    existing_vote = Votes.query.filter_by(user_id=current_user.id, scheme_id=scheme_id).first()

    if existing_vote:
        existing_vote.downvote += 1
    else:
        vote = Votes(user_id=current_user.id, scheme_id=scheme_id, upvote=0, downvote=1)
        db.session.add(vote)

    db.session.commit()
    flash("Your downvote has been recorded.", "success")
    return redirect(request.referrer or url_for('cengov'))



@app.route('/View')
def view():
    completed_promises = [
        "100% electrification of villages",
        "Construction of 100 smart cities",
        "Swachh Bharat Mission for clean India",
        "Digital India initiative",
        "Ayushman Bharat healthcare for poor"
    ]

    not_completed_promises = [
        "Doubling farmers' income by 2022",
        "Make in India to boost manufacturing",
        "Affordable housing for all by 2022",
        "New Education Policy implementation",
        "Self-reliant India (Atmanirbhar Bharat)"
    ]

    promises_data = [
        {"promise": "Promise A", "complaints": 50},
        {"promise": "Promise B", "complaints": 30},
        {"promise": "Promise C", "complaints": 25},
        {"promise": "Promise D", "complaints": 20},
        {"promise": "Promise E", "complaints": 15},
        {"promise": "Promise F", "complaints": 10},
        {"promise": "Promise G", "complaints": 5},
    ]

    sorted_promises = sorted(promises_data, key=lambda x: x["complaints"], reverse=True)
    top5 = sorted_promises[:5]
    top5_total = sum(item["complaints"] for item in top5)
    for item in top5:
        item["percent"] = round((item["complaints"] / top5_total) * 100, 1)

    completed_percentage = 60
    not_completed_percentage = 40
    bar_labels = [p["promise"] for p in promises_data]
    bar_data = [p["complaints"] for p in promises_data]

    return render_template('view.html',
                           completed_promises=completed_promises,
                           not_completed_promises=not_completed_promises,
                           top5=top5,
                           completed_percentage=completed_percentage,
                           not_completed_percentage=not_completed_percentage,
                           bar_labels=bar_labels,
                           bar_data=bar_data,user=current_user)

@app.route('/complaint')
def complaint():
    states_and_uts = ["Delhi", "Maharashtra", "Punjab", "Goa"]  # truncate for demo
    tenure_options = ["2024-Current", "2019-2024", "2014-2019"]
    total_complaints = 1215
    total_resolved = int(0.1 * total_complaints)
    return render_template(
        'complaint.html',
        states_and_uts=states_and_uts,
        tenure_options=tenure_options,
        total_complaints=total_complaints,
        total_resolved=total_resolved,
        complaint_number=None,user=current_user
    )

@app.route('/file-complaint', methods=['POST'])
def file_complaint():
    import random
    complaint_number = random.randint(100000, 999999)
    # Here you can save form data / files to DB or filesystem
    states_and_uts = ["Delhi", "Maharashtra", "Punjab", "Goa"]
    tenure_options = ["2024-Current", "2019-2024", "2014-2019"]
    total_complaints = 1216  # just increment for demo
    total_resolved = int(0.1 * total_complaints)
    return render_template(
        'complaint.html',
        states_and_uts=states_and_uts,
        tenure_options=tenure_options,
        total_complaints=total_complaints,
        total_resolved=total_resolved,
        complaint_number=complaint_number,user=current_user
    )


@app.route('/Login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("profile"))
        else:
            return "Invalid credentials" 
    return render_template('login.html')

@app.route('/Signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        fullname=request.form['name']
        emailid=request.form['email']
        passw=request.form['password']
        phone_no=request.form['phone']
        aadhar_no=request.form['aadhaar']

        new_user=User(name=fullname,email=emailid,phone=phone_no,password=passw,aadhar=aadhar_no)
        db.session.add(new_user)
        db.session.commit()
        return redirect ('/Login') 

    return render_template('signup.html')

@app.route('/Central-Govt')
def cengov():
    manifestos=Manifesto.query.all()
    return render_template('cengov.html',manifesto=manifestos)

@app.route('/State-Govt')
def stagov():
    return render_template('stagov.html')

@app.route('/profile',methods=['POST','GET'])

def profile():
    voted_promises = ["Free WiFi for Students", "Public Transport Upgrade"]
    filed_complaints = ["Road Repairs Pending", "Delayed Scholarship Disbursement"]
    return render_template(
        'profile.html',
        voted_promises=voted_promises,
        filed_complaints=filed_complaints,user=current_user
    )

if __name__ == '__main__':
    app.run(debug=True)
