from flask import Flask, render_template,url_for,request,redirect,session
from flask_mysqldb import MySQL
import MySQLdb.cursors

#database name: flask_db

#table name: admins
#column name: id, type: int, Extra: AUTO_INCREMENT
#column name: username, type: varchar, length: 255
#column name: password, type: varchar, length: 255

#table name: news
#column name: id, type: int, Extra: AUTO_INCREMENT
#column name: title, type: text
#column name: news, type: text






app = Flask(__name__)
app.secret_key = 'qweqwe'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_db'

mysql = MySQL(app)



@app.route('/')
def index():

    return render_template("index.html")


    

@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        stmt = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        stmt.execute('INSERT INTO users VALUES (NULL,%s,%s,%s)', (firstname,lastname,email))
        mysql.connection.commit()
        return redirect(url_for('registration_success'))
    return render_template("register.html")



@app.route('/registration_success')
def registration_success():
    return render_template("registration_success.html")

@app.route('/news',methods=['GET'])
def news():
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM news ORDER BY id desc")
    result = cursor.fetchall()
    return render_template("news.html",data = result)

@app.route('/admin_login',methods = ['GET','POST'])
def admin_login():
    message = ''
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admins WHERE username = %s AND password = %s',(username,password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['id']
            session['username'] = user['username']
            message = "Login Success!"
            return redirect(url_for('admin'))
        else:
            message = "Username and password does not match."
    return render_template("admin_login.html")


@app.route('/admin',methods = ['GET','POST'])
def admin():
    if request.method == "POST":
        title = request.form['title']
        news = request.form['news']
        stmt = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        stmt.execute('INSERT INTO news VALUES (NULL,%s,%s)', (title,news))
        mysql.connection.commit()
        return redirect(url_for('news_sent'))
    return render_template("admin.html")

@app.route('/news_sent')
def news_sent():
    return render_template("news_sent.html")

@app.route('/update_page')
def update_page():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM news ORDER BY id desc")
    result = cursor.fetchall()
    return render_template("update_page.html",data = result)


@app.route('/update_news',methods = ['GET','POST'])
def update_news():
    id = request.form['title_id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM news where id = %s",[id])
    result = cursor.fetchone()


             
    return render_template("update_news.html",result=result)

@app.route('/update',methods = ['GET','POST'])
def update():

    if request.method == "POST":

        new_id = request.form['id']
        new_title = request.form['title']
        new_news = request.form['news']
        stmt = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        stmt.execute('UPDATE news SET title = %s, news = %s WHERE id = %s',(new_title,new_news,new_id))
        mysql.connection.commit()
    return render_template("update.html")

@app.route('/delete',methods = ['GET','POST'])
def delete():
    if request.method == "POST":

        new_id = request.form['id']
        stmt = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        stmt.execute('DELETE FROM news WHERE id = %s ',[new_id])
        mysql.connection.commit()
    return render_template("delete.html")


    
    
    
    



    




if __name__ == "__main__":
    app.run(debug=True)
