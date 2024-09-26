from flask import Flask,render_template, request, flash,redirect,url_for, session
import mysql.connector
from flask_session import Session



database=mysql.connector.connect(host="localhost",
                                 user="root",
                                 password="Harish@2005",
                                 database="train_ticket_booking")
db=database.cursor()

app = Flask(__name__)

app.secret_key = '%KCP{NB@^f7idgfjykO;ppip>Uk}'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


#<---------------------------------------SIGNUP---------------------------------------->

@app.route('/signup',methods=["POST","GET"])
def hello():

    if request.method == "GET":

        return render_template('signup.html')
    
    else:
        print("POST")

        #GET DATA FROM USER REGISTRATION PAGE

        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        print(username,password,email,confirm_password)
        
    
    
        #EMAIL LIST CONVERTER
        email_list=list(email)

         #CHECK SAME USERNAME IN DATABASE...
        db.execute("SELECT USER_NAME FROM USER_DETAILS WHERE USER_NAME='{0}';".format(username))
        db_username=db.fetchall()
        if db_username==[]:
           username_found=0
        else:
           username_found=1

    #CHECK SAME EMAIL IN DATABASE...

        db.execute("SELECT EMAIL FROM USER_DETAILS WHERE EMAIL='{0}';".format(email))
        db_email=db.fetchall()
        if db_email==[]:
            email_found=0
        else:
            email_found=1
     
     #VALIDATION 

     #USERNAME VALIDATION..

        if username=="":
            flash("Username can't be empty.." )
            return render_template("signup.html")
    
        elif len(username)<6 or len(username)>16:
            flash("Username must be 7 to 15 characters")
            return render_template("signup.html")
        elif username_found==1:
            flash("Username already taken,Try another Username..")
            return render_template("signup.html")
    
    #EMAIL VALIDATION...

        if email=="":
            flash("E-mail can't be empty..")
            return render_template("signup.html")
    
        elif len(email) <12 or len(email)>54:
            flash("E-mail must be 11 to 53 characters")
            return render_template("signup.html")
        elif email_list[-1] !="m" or email_list[-2] !="o" or email_list[-3] !="c" or email_list[-4] !="." or email_list[-5] !="l" or email_list[-6] !="i" or email_list[-7] !="a" or email_list[-8] !="m" or email_list[-9] !="g" or email_list[-10] !="@":
            flash("Invalid email address")
            return render_template("signup.html")
        elif email_found==1:
            flash("Email already taken,Try another Email..")
            return render_template("signup.html")
    
    #PASSWORD VALIDATION....

        elif len(password)<6 or len(password)>25:
           flash("Password must contain 5 to 24 characters")
           return render_template("signup.html")
        elif password !=confirm_password:
           flash("Password and Confirm Password doesn't match..")
           return render_template("signup.html")
    
    #STORE INFORMATION IN DATABASE

        else:
           db.execute("INSERT INTO USER_DETAILS(USER_NAME, EMAIL, PASSWORD) VALUES ('{0}', '{1}', '{2}');".format(username, email, password))
           database.commit()
           flash("Green")
           return redirect(url_for("login"))
        print("hello")
        return render_template('signup.html')

    return "post method"

    
   
     #<----------------------------------LOGIN-------------------------------->

@app.route('/login',methods=["POST","GET"])
def login():

    print(request.method)
    if request.method=="GET":
        print("login")
        return render_template("login.html")
    elif request.method=="POST":
        print("POST")

        #GET DATA FROM LOGIN PAGE

        username=request.form['username']
        password=request.form['password']

        #GET USERNAME AND PASSWORD FROM DATABASE..

        db.execute("SELECT USER_NAME FROM USER_DETAILS WHERE USER_NAME='{0}';".format(username))
        db_username=db.fetchall()
        if db_username ==[]:
            username_found=0
        else:
            db.execute("SELECT PASSWORD FROM USER_DETAILS WHERE USER_NAME='{0}';".format(username))
            db_password=db.fetchone()
            username_found=1

        if username=="":
            flash("Username can't be Empty..")
            return render_template("login.html") 
        elif password=="":
            flash("Password can't be Empty..")
            return render_template("login.html")
        elif username_found==0:
            flash("Username Not Found..")
            return render_template("login.html")
        elif password!=db_password[0]:
            flash("Password does not match for the Username..")
            return render_template("login.html")
        else:
            session["username"]=username
            return redirect(url_for('home'))
            return render_template('login.html')
            
    return render_template("homepage.html")


 # Check if the user is logged in
    if "username" in session:
        username = session["username"]
        if request.method == "GET":
            return render_template("homepage.html", username=username)
        elif request.method == "POST":
            # Handle form submission or other actions
            # ...
            return "Post method"
    else:
        # User is not logged in, redirect to login page
        return redirect(url_for("login"))

#<--------------------------------HOMEPAGE------------------------------>


@app.route('/home',methods=["GET","POST"])
def home():

    # Fetch departure and arrival details from the database
    db.execute("SELECT DISTINCT DEPARTURE FROM TRAIN_DETAILS")
    departure_results = db.fetchall()

    db.execute("SELECT DISTINCT ARRIVAL FROM TRAIN_DETAILS")
    arrival_results = db.fetchall()

   

    # Convert the results to a list of strings
    departure_cities = [departure[0] for departure in departure_results]
    arrival_cities = [arrival[0] for arrival in arrival_results]

    # Render the homepage template and pass the departure and arrival cities to it
    return render_template('homepage.html', departure_cities=departure_cities, arrival_cities=arrival_cities)




@app.route('/search', methods=['POST'])
def search():
    # Retrieve the selected departure, arrival, and travel date from the form
    departure = request.form.get('departure')
    arrival = request.form.get('arrival')
    travel_date = request.form.get('travelDate')

    # Perform the search operation using the retrieved values
    query = "SELECT TRAIN_ID, TRAIN_NAME, DEPARTURE, ARRIVAL, DEPARTURE_TIME, ARRIVAL_TIME, DURATION, DATEOFTRAVEL FROM TRAIN_DETAILS WHERE DEPARTURE = '{}' AND ARRIVAL = '{}' AND DATEOFTRAVEL = '{}'".format(departure, arrival, travel_date)
    db.execute(query)
    search_results = db.fetchall()
    print(query)
    print(search_results)  # Print search results for debugging

    query = "SELECT BUSINESS_CLASS_SEATS, A_TIER, B_TIER, TOTAL_SEATS, FARE FROM TRAIN_DETAILS WHERE DEPARTURE='{}' AND ARRIVAL='{}' AND DATEOFTRAVEL='{}'".format(departure, arrival, travel_date)
    db.execute(query)
    fare_results = db.fetchall()
    print(query)
    
    return render_template("booking.html", data_1=search_results, data_2=fare_results, departure=departure, arrival=arrival, travel_date=travel_date)



#<--------------------------TICKET--------------------------->

@app.route('/ticket', methods=['POST'])
def ticket():
    # Retrieve the selected departure, arrival, and travel date from the form
    departure = request.form.get('departure')
    arrival = request.form.get('arrival')
    travel_date = request.form.get('travelDate')
    
    # Retrieve the selected seat class
    selected_seat_class = request.form.get('selected_seat_class')
    
    # Perform the search operation and retrieve fare information using the retrieved values
    query = "SELECT TRAIN_ID, TRAIN_NAME, DEPARTURE, ARRIVAL, DEPARTURE_TIME, ARRIVAL_TIME, DURATION, DATEOFTRAVEL FROM TRAIN_DETAILS WHERE DEPARTURE = '{}' AND ARRIVAL = '{}' AND DATEOFTRAVEL = '{}'".format(departure, arrival, travel_date)
    db.execute(query)
    search_results = db.fetchall()

    query = "SELECT BUSINESS_CLASS_SEATS, A_TIER, B_TIER, TOTAL_SEATS, FARE FROM TRAIN_DETAILS WHERE DEPARTURE='{}' AND ARRIVAL='{}' AND DATEOFTRAVEL='{}'".format(departure, arrival, travel_date)
    db.execute(query)
    fare_results = db.fetchall()

    return render_template("ticket.html", search_results=search_results, fare_results=fare_results, selected_seat_class=selected_seat_class)


#<-------------------------PAYMENT------------------------------>
@app.route('/payment')
def payment():
    return render_template("payment.html")


#<-----------------------------LOGOUT------------------------------------->
@app.route('/logout')
def logout():
    # Clear the session and log out the user
    session.clear()
    return redirect(url_for("login"))


app.run(debug=True)