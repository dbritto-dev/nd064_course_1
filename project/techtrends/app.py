import sqlite3
import logging
import datetime

from flask import Flask, jsonify, render_template, request, url_for, redirect, flash

logging.basicConfig(level=logging.DEBUG, format=f'%(levelname)s:%(name)s:%(message)s')

class Database:
    _db_connection_count = 0

    @staticmethod
    def get_db_connection():
        # Function to get a database connection.
        # This function connects to database with the name `database.db`
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row

        Database._db_connection_count += 1

        return connection

    @staticmethod
    def get_db_connection_count():
        return Database._db_connection_count

    @staticmethod
    def has_access():
        try:
            with Database.get_db_connection() as _:
                return True
        except:
            return False

    @staticmethod
    def has_table(table_name: str):
        try:
            with Database.get_db_connection() as connection:
                connection.execute(
                    f'SELECT * FROM {table_name} LIMIT 1').fetchone()
                return True
        except:
            return False


class Post:
    @staticmethod
    def get_post_count() -> int:
        with Database.get_db_connection() as connection:
            post_count = connection.execute(
                'SELECT COUNT(*) as count FROM posts').fetchone()['count']
            return post_count

    @staticmethod
    def get_post(post_id: int):
        # Function to get a post using its ID
        with Database.get_db_connection() as connection:
            post = connection.execute(
                'SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
            return post

    @staticmethod
    def get_posts():
        with Database.get_db_connection() as connection:
            posts = connection.execute('SELECT * FROM posts').fetchall()
            return posts

    @staticmethod
    def create_post(title: str, content: str):
        with Database.get_db_connection() as connection:
            connection.execute(
                'INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            connection.commit()


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    # Define the main route of the web application
    posts = Post.get_posts()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id: int):
    # Define how each individual article is rendered
    # If the post ID is not found a 404 page is shown
    post = Post.get_post(post_id)
    timestamp = datetime.datetime.now().strftime('%Y/%m/%d, %H:%M:%S')
    
    if post is None:
        app.logger.info(f'{timestamp}, Article with {post_id} not found!')

        return render_template('404.html'), 404
    else:
        post_title = post['title']
        app.logger.info(f'{timestamp}, Article "{post_title}" retrieved!')

        return render_template('post.html', post=post)


@app.route('/about')
def about():
    app.logger.info(f'The "About Us" page is retrieved!')
    # Define the About Us page
    return render_template('about.html')


@app.route('/create', methods=('GET', 'POST'))
def create():
    # Define the post creation functionality
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            timestamp = datetime.datetime.now().strftime('%Y/%m/%d, %H:%M:%S')
            app.logger.info(f'{timestamp}, A new article "{title}" is created!')

            Post.create_post(title, content)

            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/healthz')
def healthz():
    if not Database.has_access():
        return jsonify('result: ERROR - unhealthy'), 500

    if not Database.has_table('posts'):
        return jsonify('result: ERROR - unhealthy'), 500

    return jsonify('result: OK - healthy')


@app.route('/metrics')
def metrics():
    db_connections_count = Database.get_db_connection_count()
    post_count = Post.get_post_count()
    return {"db_connection_count": db_connections_count, "post_count": post_count}


# start the application on port 3111
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3111')
