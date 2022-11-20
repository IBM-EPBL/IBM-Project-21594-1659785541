from flask import Flask,url_for,redirect,render_template,request,session,sessions
import ibm_db
import ibm_db_dbi as db2
import socket
import re

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
app=Flask(__name__)
app.secret_key='a'
con=db2.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cch66020;PWD=lI1IGk5RBsX1sjkG",'','')
cur=con.cursor()
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cch66020;PWD=lI1IGk5RBsX1sjkG",'','')
@app.route('/wel')
def wel():
    return render_template("loginpage.html")
@app.route('/registerpage')
def registerpage():
    return render_template("registration.html")
@app.route('/register',methods=['GET','POST']) 
def register():
    msg=''
    if request.method=='POST':
        email=request.form['email']
        passwrd=request.form['password']
        name=request.form['username']
        amount=request.form['amount']
        

        insert_sql="INSERT INTO LOGIN VALUES(?,?,?,?)"
        prep_stmt=ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt,1,email)
        ibm_db.bind_param(prep_stmt,2,passwrd)
        ibm_db.bind_param(prep_stmt,3,name)
        ibm_db.bind_param(prep_stmt,4,amount)
        ibm_db.execute(prep_stmt)
        msg='Ticket is raised successfully!'
        return render_template('expense.html',msg=msg)
    else:
        msg='Query submission Unsuccessful! Please try again later!'
        return render_template('registration.html',msg=msg)

@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg=''
    if request.method=='POST':
        username=request.form['email']
        pwd=request.form['pass']
        sql="SELECT * FROM LOGIN WHERE EMAIL=? AND PASSWORD=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,pwd)
        ibm_db.execute(stmt)
        acc=ibm_db.fetch_assoc(stmt)
        if acc:
            session['loggedin'] = True
            session['id'] = acc['USERNAME']
            session['amnt']=acc['AMOUNT']
            session['exp']=acc['EXPENSE']
            userid = acc["USERNAME"]
            session['email'] = acc["EMAIL"]
            msg='Login successful!'
            return render_template("expense.html")
        else:
            msg="Invalid username/password!"
            return render_template("loginpage.html")

@app.route('/report')
def report():
    return render_template("report.html")
@app.route('/expense')
def expense():
    return render_template("expense.html")
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/adding',methods=['GET','POST'])
def adding():
    if request.method=='POST':
        oldexpense=session['exp']
        expense=(float)(request.form['amount'])
        cat=request.form['category']
        des=request.form['note']
        name=session['id']
        amnt=session['amnt']
        insert_sql="UPDATE LOGIN SET EXPENSE=?,BALANCE=?,CATEGORY=?, DESCRIPTION=? WHERE USERNAME=?;"
        prep_stmt=ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt,1,(oldexpense+expense))
        ibm_db.bind_param(prep_stmt,2,(amnt-expense))
        ibm_db.bind_param(prep_stmt,3,cat)
        ibm_db.bind_param(prep_stmt,4,des)
        ibm_db.bind_param(prep_stmt,5,name)
        ibm_db.execute(prep_stmt)
        msg='Expense added'
        return render_template('expense.html',msg=msg)

@app.route('/display')
def display():

    cur.execute("SELECT * FROM CCH66020.LOGIN where NAME=?")

    account = cur.fetchall()
    return render_template('report.html',account=account)
if __name__ == '__main__' :
    app.run(debug=True)
