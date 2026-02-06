from flask import Flask, render_template, request, redirect, url_for, flash,jsonify,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
import base64

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Classes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "your_secret_key"  # Necessary for using flash messages
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100))
    contact = db.Column(db.String(10), nullable=True)
    dob = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profilepic = db.Column(db.LargeBinary, nullable=False)

# class UserCourses(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), db.ForeignKey('users.username'), nullable=False)
#     course_name = db.Column(db.String(100), nullable=False)
#     course_details = db.Column(db.String(255), nullable=True)
#     total_fees = db.Column(db.Float, nullable=False)
#     fees_pending = db.Column(db.Float, nullable=False)
#     fees_paid = db.Column(db.Float, nullable=False)

class Courses(db.Model):
    course_id = db.Column(db.Integer,primary_key=True)
    course_name = db.Column(db.String(100), nullable=False )
    course_price = db.Column(db.Float, nullable=False)
    course_duration = db.Column(db.Integer, nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    
    def to_dict(self):
        return{
            "course_id": self.course_id,
            "course_name": self.course_name,
            "course_price": self.course_price,
            "course_duration": self.course_duration,
            "image_data": base64.b64encode(self.image_data).decode('utf-8') if self.image_data else None
        }

class CoursePurchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    username = db.Column(db.String(100), nullable=False)  # User's name
    course_name = db.Column(db.String(100), nullable=False)  # Name of the course
    course_price = db.Column(db.Float, nullable=False)  # Price of the course
    course_purchase_date = db.Column(db.DateTime, default=datetime.utcnow)  
    course_status = db.Column(db.String(50), nullable=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    Name = db.Column(db.String(100), nullable=False)  # User's name
    Adminname=db.Column(db.String(100), nullable=False)
    password=db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()

def b64encode(value):
    return base64.b64encode(value).decode('utf-8')

app.jinja_env.filters['b64encode'] = b64encode


logineduser=''
routes = []
loginedadmin=''

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/Signup")
def signuppage():
    return render_template("Signup.html")

@app.route("/newuser", methods=["POST"])
def signup():
    name = request.form["name"]
    username = request.form["username"]
    email = request.form["email"]
    contact = request.form["contact"]
    dob = request.form["dob"]
    password = request.form["password"]
    profilepic = request.files.get('uploadpic').read()


    if not (name and username and email and contact and dob and password):
        flash("All fields are required", "error")
        return redirect(url_for("signuppage"))
    
    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        flash("Username already taken. Please choose a different username.", "error")
        return redirect(url_for("signuppage"))
    
    try:
        new_user = Users(
            name=name,
            username=username,
            email=email,
            contact=contact,
            dob=datetime.strptime(dob, "%Y-%m-%d").date(),
            password=password,
            profilepic=profilepic
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful!", "success")
        return redirect(url_for("home"))
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for("signuppage"))
    
@app.route("/newadminpage")
def adminpage():
    return render_template("adminsignup.html")

@app.route("/adminpanel")
def adminpanel():
    if session['loginedAdmin']:
        return redirect("/admin")
    return render_template("adminlogin.html")

    
@app.route("/addnewadmin", methods=["POST"])
def newadmin():
    Name = request.form["name"]
    Adminname = request.form["adminname"]
    password = request.form["password"]


    if not (Name and Adminname and  password):
        flash("All fields are required", "error")
        return redirect(url_for("/addnewadmin"))
    
    existing_user = Admin.query.filter_by(Adminname=Adminname).first()
    if existing_user:
        flash("Allready Admin exist.", "error")
        return redirect(url_for("signuppage"))
    
    try:
        new_admin = Admin(
            Name=Name,
            Adminname=Adminname,
            password=password,
        )
        db.session.add(new_admin)
        db.session.commit()
        flash("Registration successful!", "success")
        return "Registration successful!", "success"
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for("signuppage"))

@app.route("/login")
def loginpage():
    return render_template("logg.html")

@app.route("/admin")
def adminpanels():
    return render_template("admin.html")


@app.route("/logout")
def logout():
    session['logineduser'] = ""
    session['loginedAdmin']=""
    return render_template("/index.html")

@app.route("/checkuser", methods=["POST"])
def checkuser():
    username = request.form["username"]
    password = request.form["password"]

    user = Users.query.filter_by(username=username).first()
    if user and user.password == password:
        flash("Login successful!", "success")
        session['logineduser'] = user.username   
        return redirect("/")
    else:
        flash("Invalid username or password.", "error")
        session['logineduser'] = "" 
        return redirect(url_for("logg.html"))
    

@app.route("/chekadmin", methods=["POST"])
def checkadmin():
    Adminname = request.form["adminname"]
    password = request.form["password"]

    Admins = Admin.query.filter_by(Adminname=Adminname).first()
    if Admins and Admins.password == password:
        flash("Login successful!", "success")
        session['loginedAdmin'] = Admins.Adminname   
        return redirect("/admin")
    else:
        flash("Invalid username or password.", "error")
        session['logineduser'] = "" 
        return "Unable to Connect ADMIN PANEL"

@app.route("/addcoursepage")
def addcourses():
    return render_template("addcourse.html")


@app.route("/addcourse", methods=["POST"])
def addCourse():
    new_course = Courses(
    course_name= request.form["course_name"],
    course_price=request.form["course_price"],
    course_duration=request.form["course_duration"],
    image_data = request.files['uploadfile'].read()
    )

    db.session.add(new_course)
    db.session.commit()
    flash('NEW COURSE ADDED SUCCESSFULLY')
    return "course added successfully"



@app.route("/fetchcourses")
def get_courses():
    courses = Courses.query.all()
    courses_list = [course.to_dict() for course in courses]
    return jsonify(courses_list)

@app.route("/courses")
def courses():
    return render_template("courses.html")


@app.route('/deleteCourse',methods=["POST"])
def delete_course():
    Course_to_delete = Courses.query.get(request.form["course_id"])
    if Course_to_delete:
        db.session.delete(Course_to_delete)
        db.session.commit()
    return "course deleted successfully"
   

@app.route('/deletepage', methods=["GET"])
def delcourses():
    return render_template("deleteCourse.html")



@app.route('/profile')
def profileinfo():
    if 'logineduser' in session:
        username = session['logineduser']
        user = Users.query.filter_by(username=username).first()
        if user:
            courses = CoursePurchase.query.filter_by(username=username)
            return render_template("userinfo.html", user=user,courses=courses)
        else:
            flash("User not found", "error")
            return render_template("logg.html")
    else:
        flash("User not logged in", "error")
        return render_template("logg.html")#CoursePurchase
    
@app.route('/aboutus')
def Aboutus():
    return render_template("aboutus.html")
    
    

# @app.route('/buy')
# def buycourse():
#     return render_template("buycourse.html")

# @app.route('/buy')
# if 'logineduser' in session:
#     def add_user_course(username, course_name, course_details, total_fees, fees_pending, fees_paid):
#         new_course = UserCourses(
#             username=username,
#             course_name=course_name,
#             course_details=course_details,
#             total_fees=total_fees,
#             fees_pending=fees_pending,
#             fees_paid=fees_paid
#         )
#         db.session.add(new_course)
#         db.session.commit()
#         return "dkvnsdkvn"
    

@app.route('/addPython')
def addpython():
    course_name = 'Python'  # Example course name
    course = Courses.query.filter_by(course_name=course_name).first()
    if course:
        username=session['logineduser']
        course_name=course.course_name
        course_price=course.course_price

        Course_purchase = CoursePurchase(
            username=username,
            course_name=course_name,
            course_price=course_price,
            course_status="Active"
        )
        db.session.add(Course_purchase)
        db.session.commit() 
    return "Course added to your course list"


@app.route('/addC')
def addC():
    course_name = 'C'  # Example course name
    course = Courses.query.filter_by(course_name=course_name).first()
    if course:
        username=session['logineduser']
        course_name=course.course_name
        course_price=course.course_price

        Course_purchase = CoursePurchase(
            username=username,
            course_name=course_name,
            course_price=course_price,
            course_status="Active"
        )
        db.session.add(Course_purchase)
        db.session.commit() 
    return "Course added to your course list"



@app.route('/addOperatingSystem')
def addOperating():
    course_name = 'Operating System'  # Example course name
    course = Courses.query.filter_by(course_name=course_name).first()
    if course:
        username=session['logineduser']
        course_name=course.course_name
        course_price=course.course_price

        Course_purchase = CoursePurchase(
            username=username,
            course_name=course_name,
            course_price=course_price,
            course_status="Active"
        )
        db.session.add(Course_purchase)
        db.session.commit() 
    return "Course added to your course list"
   

@app.route('/api/routes', methods=['GET'])
def get_routes():
    return jsonify(routes)

@app.route('/receive_routes', methods=['POST'])
def add_route():
    new_route = request.json
    routes.append(new_route)
    return jsonify(new_route), 201


@app.route('/route')
def receive_routes():
    for route in routes:
        print(f"route issss {route}")
        # app.add_url_rule(route['route'], route['view_func'],[route['view_func']])
    return "root added"


if __name__ == "__main__":
    app.run(debug=True)
