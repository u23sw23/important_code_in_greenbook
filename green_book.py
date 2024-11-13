from flask import Flask, request, render_template, flash, url_for, redirect, session
import pymysql  #确保：1.服务里数据库都启动 2.表已经选择了框架
def get_db_connection():
    conn = pymysql.connect(
        host='127.0.0.1',
        database='test',
        port=3306
    )
    return conn

def get_posts(introduction_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)#使用 DictCursor 会让查询结果以字典（dictionary）形式返回，而不是默认的元组（tuple）形式
    sql = f"SELECT * FROM test.{introduction_id} ORDER BY timestamp DESC"
    cursor.execute(sql)
    posts = cursor.fetchall()#获取当前查询结果中的所有行，返回一个列表，列表中的每一项都是一行数据
    cursor.close()
    conn.close()
    return posts
app = Flask(__name__)
app.secret_key = '985915'
introduction_data = {
    'happy_monk_restaurant': {
        'name': 'Happy Monk Restaurant',
        'image_url': '../static/public/Happy Monk Restaurant.jpg',
        'description': 'This is a detailed introduction to easy_join_coffee'
    },
    'over_easy_restaurant': {
        'name': 'Over easy restaurant',
        'image_url': '../static/public/Over easy restaurant.jpg',
        'description': 'This is a detailed introduction to puppy_coffee'
    },
    'CHILLAX Restaurant': {
        'name': 'CHILLAX Restaurant',
        'image_url': '../static/public/CHILLAX Restaurant.jpg',
        'description': 'This is a detailed introduction to freedom_coffee'
    },
    'Lu Lake Park': {
        'name': 'Lu Lake Park',
        'image_url': '../static/public/Lu Lake Park.png',
        'description': 'This is a detailed introduction to Pets_Corner'
    },
    'Tianhe Wetland Park': {
        'name': 'Tianhe Wetland Park',
        'image_url': '../static/public/Tianhe Wetland Park.png',
        'description': 'This is a detailed introduction to Petco.'
    },
    'Nantou Ancient City': {
        'name': 'Nantou Ancient City',
        'image_url': '../static/public/Nantou Ancient City.png',
        'description': 'This is a detailed introduction to Pet Emporium'
    },
    'Xianhu Qingshe Hotel': {
        'name': 'Xianhu Qingshe Hotel',
        'image_url': '../static/public/Xianhu Qingshe Hotel.jpg',
        'description': 'This is a detailed introduction to Stay Mierica'
    },
    'The Victoria Hotel': {
        'name': 'The Victoria Hotel',
        'image_url': '../static/public/The Victoria Hotel.jpg',
        'description': 'This is a detailed introduction to The Grand Budapest Hotel'
    },
    'Foshan Nanhai Zhanyun Hotel': {
        'name': 'Foshan Nanhai Zhanyun Hotel',
        'image_url': '../static/public/Foshan Nanhai Zhanyun Hotel.jpg',
        'description': 'This is a detailed introduction to The Murray'
    },
    'HaiCheng animals hospital': {
        'name': 'HaiCheng animals hospital',
        'image_url': '../static/public/HaiCheng animals hospital.jpg',
        'description': 'This is a detailed introduction to The Murray'
    },
    'Aibesi Animal Hospital': {
        'name': 'Aibesi Animal Hospital',
        'image_url': '../static/public/Aibesi Animal Hospital.jpg',
        'description': 'This is a detailed introduction to The Murray'
    },
    'Shi Jia Animals hospital': {
        'name': 'Shi Jia Animals hospital',
        'image_url': '../static/public/Shi Jia Animals hospital.png',
        'description': 'This is a detailed introduction to The Murray'
    }
}

@app.route('/introduction/<introduction_id>', methods=['GET', 'POST'])
def introduction_detail(introduction_id):
    # 获取场所信息
    place_info = introduction_data.get(introduction_id)
    if not place_info:
        flash('The location information was not found.')
        return redirect(url_for('home'))
    # 获取评论列表
    try:
        posts = get_posts(introduction_id)
    except Exception as e:
        posts = []
        flash(f'获取评论失败：{str(e)}')

    if request.method == 'POST':
        username = request.form['username']
        content = request.form['content']
        rating = request.form['rating']  # 获取评分
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = f"INSERT INTO test.{introduction_id} (username, content, rating, timestamp) VALUES (%s, %s, %s, NOW())"
            cursor.execute(sql, (username, content, rating))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('introduction_detail', introduction_id=introduction_id))#将当前的 introduction_id 值作为参数传递给路由，告诉Flask要重新定向到哪个页面
        except Exception as e:
            flash(f'提交评论失败：{str(e)}')

    # GET 请求时渲染模板
    return render_template('introduction_detail.html',  
                           introduction=place_info,  # 改为与模板中使用的变量名一致
                           posts=posts,
                           introduction_id=introduction_id)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            conn = None
            cur = None
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute('INSERT INTO test.login_test (username, password, email) VALUES (%s, %s, %s)', (username, password, email))
                conn.commit()
                return render_template('log_in_page.html')
            except Exception as e:
                flash('登录失败：' + str(e))
            finally:
                cur.close()
                conn.close()
            return render_template('log_in_page.html') #原先登陆界面，上面都是
        else:
            username = request.form['username'] #这行代码从请求的表单数据中获取 name="username"的值，并将其赋值给变量 username
            password = request.form['password'] #request.form 是一个类似字典的对象，包含了所有的表单数据
            conn = None
            cur = None
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute('SELECT * FROM test.login_test WHERE username = %s AND password = %s', (username, password))
                result = cur.fetchone() #是一个游标（cursor）对象的方法，用于从结果集中获取第一条记录
                print(f"用户名为{username}密码为{password}的用户刚刚登陆了网站")  # 打印用户名和密码到控制台（也就是这里）
                if result:
                    return render_template('home.html') #跳转到主页
                else:
                    flash('Username or password is incorrect!')
            except Exception as e:
                flash('登录出现问题：' + str(e))
            finally:
                cur.close()
                conn.close()
            return render_template('log_in_page.html') # 重新渲染登录页面
    else:
        return render_template('log_in_page.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/login')
def login1():
    return render_template('log_in_page.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
