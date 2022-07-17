#module
from flask import Flask, render_template, request, session
from flask_bcrypt import Bcrypt
import datetime
import flask
import pymysql

#flask
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["SECRET_KEY"] = b'changeme!'
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=60)
app.config['BCRYPT_LEVEL'] = 10

#html path define
HTML_PATH_MAIN = './main.html'
HTML_PATH_STUDY = './board/study.html'
HTML_PATH_ANON = './board/anon.html'
HTML_PATH_STOCK = './board/stock.html'
HTML_PATH_REGISTER = './sign/register.html'
HTML_PATH_LOGIN = './sign/login.html'
HTML_PATH_WRITE = './write/write.html'

#mysql
def db_connector(sql_command):
    MYSQL_DB = {
        'user'     : 'dbuser',
        'password' : 'abcd1234',
        'host'     : 'localhost',
        'port'     : '3306',
        'database' : 'dblife'
    }
    db = pymysql.connect(
        host=MYSQL_DB['host'],
        port=int(MYSQL_DB['port']),
        user=MYSQL_DB['user'],
        passwd=MYSQL_DB['password'],
        db=MYSQL_DB['database'],
        charset='utf8'
    )
    cursor = db.cursor()
    cursor.execute(sql_command)
    result = cursor.fetchall()
    db.commit()
    db.close()
    return str(result).replace("(", "").replace(")", "").replace("'", "").replace(',', '').rstrip()

def checklogin():
    if 'user' in session:
        return True
    return False

@app.route('/', methods=['GET']) 
def index():
    return render_template(HTML_PATH_MAIN)

#signin
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method =='GET':
        if checklogin():
            return render_template(HTML_PATH_MAIN, username=session['user'])
        return render_template(HTML_PATH_REGISTER)
    elif request.method =='POST':
        #form.get
        userid = request.form.get('id')
        usernickname = request.form.get('usernick')
        userpw = request.form.get('password')
        reuserpw = request.form.get('repassword')
        ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        useragent = request.headers.get('User-Agent')

        #connect_db
        if not (userid and usernickname and userpw and reuserpw and ip_address and useragent):
            return render_template(HTML_PATH_REGISTER, ErrorTitle="ERROR! ", ErrorMessage="모두 입력해주세요.")
        if userpw != reuserpw:
            return render_template(HTML_PATH_REGISTER, ErrorTitle="ERROR! ", ErrorMessage="비밀번호가 다릅니다.")
        
        #password hashing
        pw_hash = bcrypt.generate_password_hash(userpw).decode('utf-8')

        checkusername = db_connector(f'''SELECT userid FROM usertbl WHERE userid="{userid}";''')
        if checkusername == "":
            db_connector(f"INSERT INTO usertbl(userid, usernick, userpw, userip, useragent) VALUES('{userid}', '{usernickname}', '{pw_hash}', '{ip_address}', '{useragent}');")
            return render_template(HTML_PATH_LOGIN, ErrorTitle="NOTICE! ", ErrorMessage="가입에 성공하였습니다.")
        else:
            return render_template(HTML_PATH_REGISTER, ErrorTitle="ERROR! ", ErrorMessage="아이디가 이미 존재합니다.")

@app.route('/back2register', methods=['GET'])
def back2register():
    return render_template(HTML_PATH_REGISTER)

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if checklogin():
            return render_template(HTML_PATH_MAIN, username=session['user'])
        return render_template(HTML_PATH_LOGIN)
    elif request.method == 'POST':
        #form.get
        userid = request.form.get('id')
        userpw = request.form.get('password')

        #connect_db
        if not (userid and userpw):
            return render_template(HTML_PATH_LOGIN, ErrorTitle="ERROR! ", ErrorMessage="모두 입력해주세요.")
        
        #password hashing
        realuserpw = db_connector(f'''SELECT userpw FROM usertbl WHERE userid="{userid}";''')
        if bcrypt.check_password_hash(realuserpw, userpw):
            session['user'] = userid
            return render_template(HTML_PATH_MAIN, username=session['user'])
        else:
            return render_template(HTML_PATH_LOGIN, ErrorTitle="ERROR! ", ErrorMessage="아이디 혹은 비밀번호가 맞지 않습니다.")
    
@app.route('/back2login', methods=['GET'])
def back2login():
    return render_template(HTML_PATH_LOGIN)

#logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return render_template(HTML_PATH_MAIN)

@app.route('/logoutstudy', methods=['GET'])
def logoutstudy():
    session.pop('user', None)
    return render_template(HTML_PATH_STUDY)

@app.route('/logoutanon', methods=['GET'])
def logoutanon():
    session.pop('user', None)
    return render_template(HTML_PATH_ANON)

@app.route('/logoutstock', methods=['GET'])
def logoutstock():
    session.pop('user', None)
    return render_template(HTML_PATH_STOCK)

#board
@app.route('/study', methods=['GET'])
def study():
    return render_template(HTML_PATH_STUDY)

@app.route('/anon', methods=['GET']) 
def anon():
    return render_template(HTML_PATH_ANON)

@app.route('/stock', methods=['GET']) 
def stock():
    return render_template(HTML_PATH_STOCK)

#write
@app.route('/write', methods=['GET', 'POST']) 
def write():
    if request.method == 'GET':
        if checklogin():
            return render_template(HTML_PATH_WRITE, username=session['user'])
        else:
            return render_template(HTML_PATH_LOGIN)
    elif request.method == 'POST':

        #form.get
        title = request.form.get('title')
        content = request.form.get('content')
        ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        useragent = request.headers.get('User-Agent')
        userid = session['user']

        #connect_db
        if not (title and content and ip_address and useragent and userid):
            return render_template(HTML_PATH_MAIN, username=session['user'])
        db_connector(f"INSERT INTO posttbl(posttitle, postcontent, userid, userip, useragent) VALUES('{title}', '{content}', '{userid}', '{ip_address}', '{useragent}');")

@app.route('/writecomment', methods=['POST'])
def writecomment():

    #form.get
    content = request.form.get('content')
    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    useragent = request.headers.get('User-Agent')
    userid = session['user']

    #connect_db
    if not (content and ip_address and useragent and userid):
        return render_template(HTML_PATH_MAIN, username=session['user'])
    db_connector(f"INSERT INTO usertbl(postcontent, userid, userip, useragent) VALUES('{content}', '{userid}', '{ip_address}', '{useragent}');")

if __name__ == '__main__':
    app.run(host="localhost", port="3000",debug=False, threaded=True)