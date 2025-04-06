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
    if request.method == "GET":
        return render_template("signup.html")
    
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
                return render_template("signup.html", error="Error: That username already exist")
        for application in applicationsDB:
            if request.form['username'] == application[usernameIndex]:
                return render_template("signup.html", error="Error: That username is currently pending")
        if request.form['username'] == adminDB[0][usernameIndex]:
            return render_template("signup.html", error="Error: Invalid username")
        
        
        
        conn.execute(text("INSERT INTO applications "
                        "    (username, password, first_name, last_name, ssn, phone_num)"
                        "VALUES "
                        f"('{request.form['username']}', '{request.form['password']}', '{request.form['first_name']}', "
                        f" '{request.form['last_name']}', '{request.form['ssn']}', '{phone_num}')"))
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
            # return render_template("signup.html", error="Error")

        return render_template("signup.html", success="Success")

# ---------------- #
# -- LOGIN PAGE -- #
# ---------------- #

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        admin_username = dict( conn.execute(text("SELECT username, password FROM admin")).all() )
        users_username = dict( conn.execute(text("SELECT username, password FROM users")).all() )
        
        if username in admin_username.keys() and admin_username[username] == password:
            print(logIntoDB('admin', username, password))

        elif username in users_username.keys() and users_username[username] == password:
            logIntoDB('user', username, password)
        else:
            return render_template("login.html", error="Error: Invalid username or password")
        
        return render_template("login.html", success="Login success")
      
      
# ------------------ #
# -- ACCOUNT PAGE -- #
# ------------------ #

@app.route('/account', methods=['GET'])
def account():
    current = getCurrentUser()
    users = list(conn.execute(text('SELECT acc_num, CONCAT(first_name, " ", last_name), username, phone_num FROM users WHERE acc_num = :current;'), {'current': current}).fetchone())
    address = list(conn.execute(text('SELECT CONCAT(street_addr, ", ", city, ", ", state, " ", zip_code, " ", country) FROM addresses WHERE acc_num = :current;'), {'current': current}).fetchone())
    print(current)
    print(users)
    print(address)
    return render_template('account.html', accounts = users, address = address)


# ------------------ #
# -- BALANCE PAGE -- #
# ------------------ #

@app.route('/balance', methods=['GET'])
def balance():
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
    accountNum = request.form.get('account')
    amount = request.form.get('addAmount')
    amount = round(float(amount), 2)
    print('account:', accountNum)
    print('amount:', amount)

    try:
        amount = amount * 100
        conn.execute(text('UPDATE users SET balance = balance + :amount WHERE acc_num = :account'), {'amount': amount, 'account': accountNum})
        conn.commit()
        print('success')
    except Exception as e:
        print('error updating balance:', e)

    return redirect(url_for('balance'))

# --------------------- #
# -- SEND MONEY PAGE -- # 
# --------------------- #

@app.route('/send_money', methods=['GET', 'POST'])
def send_money():
    current = getCurrentUser()
    balanceInfo = conn.execute(text('SELECT acc_num, balance FROM users WHERE username = :current'), {'current': current}).all()
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
    fromAccount = request.form.get('accounts')
    toAccount = request.form.get('toAccounts')
    amountNum = request.form.get('sendAmount')
    amount = round(float(amountNum), 2)

    try:
        amount *= 100
        conn.execute(text('UPDATE users SET balance = balance + :amount WHERE acc_num = :to'), {'to': toAccount, 'amount': amount})
        conn.execute(text('UPDATE users SET balance = balance - :amount WHERE acc_num = :from'), {'from': fromAccount, 'amount': amount})
        conn.commit()
    except Exception as e:
        print('error updating balance:', e)

    return redirect(url_for('send_money'))


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
            result = conn.execute(text( "SELECT acc_num FROM users "
                                       f"WHERE username = '{username}' AND password = '{password}'")).all()

        print(f"logIntoDB result variable = {result}")
        
        if not result:                                                                
            return "no users"
        
        stored_id = result[0][0]                                                      

        conn.execute(                                                                 
            text("UPDATE loggedin SET acc_num = :acc_num, admin_id = :admin_id"),
                {'acc_num': stored_id if accType == 'user' else None,
                'admin_id': stored_id if accType == 'admin' else None}
        )                                             
        conn.commit()                                                                 

        return "Executed function logIntoDB fully"

def loggedIntoType():                                                                    
    """Returns either 'user', 'admin', or None"""
    value = conn.execute(text("SELECT * FROM loggedin")).all()
    
    if value[0][0]:                                                                      
        return "user"                                                                
    elif value[0][1]:                                                              
        return "admin"                                                          
    else:                                                                               
        return None                                                                     

def getCurrentUser():                                                                   
    """Returns either the admin_id, acc_num, or None"""
    user = conn.execute(text('SELECT * FROM loggedin;')).all()                          

    if loggedIntoType() == 'user':                                               
        return user[0][0]                                                               
    elif loggedIntoType() == 'admin':                                             
        return user[0][1]      

def realBalance(int):
    int = int / 100
    number = '{:.{}f}'.format(int, 2)  
    print('the number:', float(number))
    return float(number)                                                      


if __name__ == "__main__":
    app.run(debug=True)