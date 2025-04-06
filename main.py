from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, text, insert, Table, MetaData, update
from scripts.shhhh_its_a_secret import customHash
# from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
# from flask_sqlalchemy import SQLAlchemy

# npm install imask for js in balance.html

app = Flask(__name__)                                                                   # initiates flask
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:cset155@localhost/cset170final"


conn_str = "mysql://root:cset155@localhost/cset170final"                                
engine = create_engine(conn_str, echo=True)                                             
conn = engine.connect()                                                                 


# For login session. Will continue to try and get this to work if we have extra time
"""
login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)
class User(UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
"""

# --------------- #
# -- HOME PAGE -- #
# --------------- #

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')


# ----------------- #
# -- SIGNUP PAGE -- #
# ----------------- #

@app.route('/signup', methods=["GET", "POST"])
def signup():
    admin = loggedIntoType() == 'admin'
    if request.method == "GET":
        return render_template("signup.html", admin = admin)
    
    if request.method == "POST":
        # try:
        usersDB = conn.execute(text("SELECT username, password, first_name, last_name, ssn, phone_num "
                                    "FROM users")).all()
        applicationsDB = conn.execute(text("SELECT username, password, first_name, last_name, ssn, phone_num "
                                        "FROM applications")).all()
        adminDB = conn.execute(text("SELECT username, password "
                                        "FROM admin")).all()
        usernameIndex, passwordIndex, first_nameIndex = 0, 1, 2
        last_nameIndex, ssnIndex, phone_numIndex = 3, 4, 5
        phone_num = request.form['phone_num'] if request.form['phone_num'] else 'NULL'

        for user in usersDB:
            if request.form['username'] == user[usernameIndex]:
                return render_template("signup.html", admin = admin, error="Error: That username already exist")
        for application in applicationsDB:
            if request.form['username'] == application[usernameIndex]:
                return render_template("signup.html", admin = admin, error="Error: That username is currently pending")
        if request.form['username'] == adminDB[0][usernameIndex]:
            return render_template("signup.html", admin = admin, error="Error: Invalid username")
        
        
        
        conn.execute(text("INSERT INTO applications "
                        "    (username, password, first_name, last_name, ssn, phone_num)"
                        "VALUES "
                        f"('{request.form['username']}', '{customHash(request.form['password'])}', '{request.form['first_name']}', "
                        f" '{request.form['last_name']}', '{request.form['ssn']}', {phone_num})"))
        conn.commit()
        appli_id = conn.execute(text("SELECT appli_num FROM applications "
                                f"WHERE username = '{request.form['username']}'")).all()[0][0]
        conn.execute(text("INSERT INTO addresses "
                            "(appli_num, street_addr, city, state, zip_code) "
                            "VALUES "
                            f"({appli_id}, '{request.form['street_addr']}', '{request.form['city']}', "
                            f"'{request.form['state']}', '{request.form['zip_code']}')"))
        conn.commit()
        # except:
            # return render_template("signup.html", admin = admin, error="Error")

        return render_template("signup.html", admin = admin, success="Success. Your account now needs accepted")


# ---------------- #
# -- LOGIN PAGE -- #
# ---------------- #

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        username = request.form['username']
        password = customHash(request.form['password'])
        admin_username = dict( conn.execute(text("SELECT username, password FROM admin")).all() )
        users_username = dict( conn.execute(text("SELECT username, password FROM users")).all() )
        
        if username in admin_username.keys() and admin_username[username] == password:
            print(logIntoDB('admin', username, password))

        elif username in users_username.keys() and users_username[username] == password:
            logIntoDB('user', username, password)
        else:
            return render_template("login.html", error="Error: Invalid username or password")
        
        return render_template("login.html", success="Login success")
    
# -- sign out -- #

@app.route('/signout')
def signout():
    conn.execute(
        text('UPDATE loggedin SET username = NULL, admin_id = NULL ' \
        'WHERE username IS NOT NULL OR admin_id IS NOT NULL;')
    )
    conn.commit()
    return redirect('/login')
      
      
# ------------------ #
# -- ACCOUNT PAGE -- #
# ------------------ #

@app.route('/account', methods=['GET', "POST"])
def account():
    if loggedIntoType() == 'admin' or loggedIntoType() == None:
        return redirect(url_for('home'))
    current = getCurrentUser()
    users = list(conn.execute(text('SELECT acc_num, CONCAT(first_name, " ", last_name), username, phone_num FROM users WHERE username = :current;'), {'current': current}).all())
    address = list(conn.execute(text('SELECT CONCAT(street_addr, ", ", city, ", ", state, " ", zip_code) FROM addresses WHERE username = :current;'), {'current': current}).fetchone())
    if users[0][3]:
        phoneNum = formatPhoneNum(users[0][3])
    else:
        phoneNum = ''
    print(current)
    print(users)
    print(address)

    if request.method == "GET":
        return render_template('account.html', accounts = users, address = address, phone = phoneNum)
    
    elif request.method == "POST":
        u_info = conn.execute(text("SELECT username, password, first_name, last_name, ssn, phone_num "
                                              f"FROM users WHERE username = '{current}'")).all()[0]
        
        conn.execute(text("INSERT INTO users (username, password, first_name, last_name, ssn, phone_num) "
                          f"VALUES ('{u_info[0]}', '{u_info[1]}', '{u_info[2]}', '{u_info[3]}', '{u_info[4]}', {u_info[5] if u_info[5] else 'NULL'})"))
        conn.commit()
        users = list(conn.execute(text('SELECT acc_num, CONCAT(first_name, " ", last_name), username, phone_num FROM users WHERE username = :current;'), {'current': current}).all())

        return render_template('account.html', accounts = users, address = address, phone = phoneNum)


# ------------------ #
# -- BALANCE PAGE -- #
# ------------------ #

@app.route('/balance', methods=['GET'])
def balance():
    if loggedIntoType() == 'admin' or loggedIntoType() == None:
        return redirect(url_for('home'))

    current = getCurrentUser()
    balanceInfo = conn.execute(text('SELECT acc_num, balance FROM users WHERE username = :current'), {'current': current}).all()
    balanceDict = []
    for balance in balanceInfo:
        balanceNum = realBalance(balance[1])
        balanceDict.append((balance[0], balanceNum))
    print(balanceDict)
    return render_template('balance.html', balance = balanceDict)

# -- add money -- #
@app.route('/update_balance', methods=['POST', 'GET'])
def update_balance():
    if loggedIntoType() == 'admin' or loggedIntoType() == None:
        return redirect(url_for('home'))

    accountNum = request.form.get('account')
    amount = request.form.get('addAmount')
    amount = round(float(amount), 2)
    print('account:', accountNum)
    print('amount:', amount)

    try:
        amount = amount * 100
        conn.execute(
            text('UPDATE users SET balance = balance + :amount WHERE acc_num = :account'), 
            {'amount': amount, 'account': accountNum})
        conn.execute(
            text('INSERT INTO transactions (acc_num, type, related_acc, amount, description) ' 
            'VALUES (:account, "deposit", :account, :amount, "Card deposit")'),
            {'account': accountNum, 'amount': amount})
        conn.commit()
        print('success')
    except Exception as e:
        print('error updating balance:', e)

    return redirect(url_for('balance'))


# ---------------- #
# -- SEND MONEY -- #
# ---------------- #

@app.route('/send_money', methods=['GET', 'POST'])
def send_money():
    if loggedIntoType() == 'admin' or loggedIntoType() == None:
        return redirect(url_for('home'))

    current = getCurrentUser()
    balanceInfo = conn.execute(
        text('SELECT acc_num, balance FROM users WHERE username = :current'), 
        {'current': current}).all()
    balanceList = []
    balanceDict = dict(balanceInfo)
    for balance in balanceInfo:
        balanceNum = realBalance(balance[1])
        balanceList.append((balance[0], balanceNum))
    allAccounts = conn.execute(text('SELECT acc_num FROM users;')).all()
    print('balance list:', balanceList)
    print('balance info:', balanceInfo)
    print('balance dictionary:', balanceDict)
    return render_template('send_money.html', accounts = allAccounts, balance = balanceList, balanceDict = balanceDict)

@app.route('/send_money_submit', methods=['POST', 'GET'])
def send_money_submit():
    if loggedIntoType() == 'admin' or loggedIntoType() == None:
        return redirect(url_for('home'))

    fromAccount = request.form.get('accounts')
    toAccount = request.form.get('toAccounts')
    amountNum = request.form.get('sendAmount')
    amount = round(float(amountNum), 2)
    try:
        amount *= 100
        # account sending money
        conn.execute(text('UPDATE users SET balance = balance - :amount WHERE acc_num = :from;'), 
                     {'from': fromAccount, 'amount': amount})
        conn.execute(
            text('INSERT INTO transactions (acc_num, type, related_acc, amount, description) ' 
            'VALUES (:from_acc, "debit", :to_acc, :amount, "Sent money");'),
            {'from_acc': fromAccount, 'to_acc': toAccount, 'amount': amount})
        
        # account receiving money
        conn.execute(
            text('UPDATE users SET balance = balance + :amount WHERE acc_num = :to;'), 
            {'to': toAccount, 'amount': amount})
        conn.execute(
            text('INSERT INTO transactions (acc_num, type, related_acc, amount, description) ' 
            'VALUES (:to_acc, "credit", :from_acc, :amount, "Received money");'),
            {'to_acc': toAccount, 'from_acc': fromAccount, 'amount': amount})
        
        conn.commit()
    except Exception as e:
        print('error updating balance:', e)
    return redirect(url_for('send_money'))


# --------------------- #
# -- VIEW STATEMENTS -- #
# --------------------- #

@app.route('/statements')
def statements():
    if loggedIntoType() == 'admin' or loggedIntoType() == None:
        return redirect(url_for('home'))
    current = getCurrentUser()
    userAccounts = conn.execute(
        text('SELECT acc_num FROM users WHERE username = :current;'),
        {'current': current}).all()
    accountNums = [a[0] for a in userAccounts]
    
    transactions = []
    for acc in accountNums:
        rows = conn.execute(
            text('SELECT * FROM transactions WHERE acc_num = :acc ORDER BY timestamp DESC;'),
            {'acc': acc}
        ).all()
        for row in rows:
            transactions.append({
                'acc_num': row[1],
                'type': row[2],
                'amount': realBalance(row[4]),
                'other_party': row[3],
                'description': row[5],
                'timestamp': row[6]
            })
    
    return render_template('statements.html', transactions = transactions)


# ----------------------- #
# -- APPLICATIONS PAGE -- #
# ----------------------- #

@app.route("/applications", methods=["GET", "POST"])
def applications():
    appli_num_i, username_i, password_i = 0, 1, 2 
    first_name_i, last_name_i, ssn_i, phone_num_i = 3, 4, 5, 6
    applicationsDB = conn.execute(text("SELECT * FROM applications")).all()

    # Only runs this page with database if the user is an admin
    if loggedIntoType() == 'admin' or loggedIntoType() == None:
        if request.method == "GET":
            return render_template("applications.html", appliDB = applicationsDB)

        elif request.method == "POST" and 'appli_num' in request.form.keys():
            print("Is admin. Accepting application")
            appli_num = request.form['appli_num']
            print(f"appli_num: {appli_num}")

            usersDB = conn.execute(text("SELECT acc_num, username FROM users")).all()
            appli = conn.execute(text(
                "SELECT * FROM applications "
                f"WHERE appli_num = {appli_num}")).all()

            if not appli:
                return render_template("applications.html", appliDB = applicationsDB, error="Invalid application number")
                
            appli = appli[0]
            appli_phone_num = appli[phone_num_i] if appli[phone_num_i] else "NULL"
            
            for user in usersDB:
                if appli[username_i] == user[1]: # Shouldn't ever happen but who knows
                    return render_template("applications.html", appliDB = applicationsDB, error="Username already exists")

            if appli:
                conn.execute(text(
                    "INSERT INTO users "
                    "   (username, password, "
                    "    first_name, last_name, ssn, phone_num)"
                    "VALUES"
                    f"  ('{appli[username_i]}', '{appli[password_i]}', "
                    f"'{appli[first_name_i]}', '{appli[last_name_i]}', '{appli[ssn_i]}', {appli_phone_num})"))
                user_acc_num = conn.execute(text("SELECT acc_num FROM users "
                                                f"WHERE username = '{appli[username_i]}'")).all()[0][0]
                conn.execute(text(f"UPDATE addresses SET username = '{appli[username_i]}', appli_num = NULL "
                                  f"WHERE appli_num = {appli[appli_num_i]}"))
                print(f"UPDATE addresses SET username = '{appli[username_i]}', appli_num = NULL "
                                  f"WHERE appli_num = {appli[appli_num_i]}")
                conn.execute(text(f"DELETE FROM applications WHERE appli_num = {appli[appli_num_i]}"))

                conn.commit()
                applicationsDB = conn.execute(text("SELECT * FROM applications")).all()
            else: 
                return render_template("applications.html", appliDB = applicationsDB, error="Invalid application number")

            return render_template("applications.html", appliDB = applicationsDB, success="Successfully accepted user")
        
        elif request.method == "POST" and 'appli_num_delete' in request.form.keys():
            print("Is admin. Denying application")
            appli_num = request.form['appli_num_delete']
            appli = conn.execute(text(
                "SELECT * FROM applications "
                f"WHERE appli_num = {appli_num}")).all()

            if not appli:
                return render_template("applications.html", appliDB = applicationsDB, error="Invalid application number")
            appli = appli[0]

            conn.execute(text(f"DELETE FROM addresses WHERE appli_num = {appli_num}"))
            conn.execute(text(f"DELETE FROM applications WHERE appli_num = {appli_num}"))
            conn.commit()
            applicationsDB = conn.execute(text("SELECT * FROM applications")).all()
             
            return render_template("applications.html", appliDB = applicationsDB, success="Successfully denied user")

    else: # Not logged in as an admin
        print("Is not admin. :(")
        return render_template("applications.html", error="Admin not logged in")


# --------------- #
# -- FUNCTIONS -- # 
# --------------- #

def logIntoDB(accType, username=None, password=None):                                    
        """
        Logs the user into the DB. Needs accType ('admin', 'user', or None)
        You need an username and password if you are logging into an account or
        nothing if you are logging out
        """
        if accType is None:                                                           
            conn.execute(text("UPDATE loggedin "                                      
                            f"SET username = NULL, admin_id = NULL"))
            conn.commit()                                                             
            return "logged out"
        
        if accType == 'admin':
            result = conn.execute(text( "SELECT admin_id FROM admin "
                                       f"WHERE username = '{username}' AND password = '{password}'")).all()
        elif accType == 'user':
            result = conn.execute(text( "SELECT :username FROM users "
                                       f"WHERE password = :password"),
                                       {'username': username, 'password': password}).all()

        print(f"logIntoDB result variable = {result}")
        
        if not result:                                                                
            return "no users"
        
        stored_id = result[0][0]                                                      

        conn.execute(                                                                 
            text("UPDATE loggedin SET username = :username, admin_id = :admin_id"),
                {'username': stored_id if accType == 'user' else None,
                'admin_id': stored_id if accType == 'admin' else None}
        )                                             
        conn.commit()                                                                 

        return "Executed function logIntoDB fully"

def getCurrentUser():                                                                   # FUNCTION gets current user id
    user = conn.execute(text('SELECT * FROM loggedin;')).all()                          # gets data from loggedin table

    if loggedIntoType() == 'user':                                                      # if user type account
        return user[0][0]                                                               # return acc_num
    elif loggedIntoType() == 'admin' or loggedIntoType() == None:                                                   # elif admin type account
        return user[0][1]                                                               # return admin_id

def loggedIntoType():                                                                   # FUNCTION checks user type that is logged in 
    value = conn.execute(text("SELECT * FROM loggedin")).all()
    
    if value[0][0]:                                                                     # returns user type if 
        return "user"                                                                   # acc_num is not null 
    elif value[0][1]:                                                                   # returns admin type if
        return "admin"                                                                  # admin_id is not null
    else:                                                                               # else both are null and 
        return None                                                                     # is therefore not signed in

def realBalance(int):
    int = int / 100
    number = '{:.{}f}'.format(int, 2)  
    print('the number:', float(number))
    return float(number)

def formatPhoneNum(num):
    return f'({num[:3]}) {num[3:6]}-{num[6:]}'                                                      


if __name__ == "__main__":
    app.run(debug=True)