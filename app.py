import json
from flask import Flask, render_template, request, redirect, url_for
from data import PATH

app = Flask(__name__)


def get_posts() -> list:
    """
        Loads blog posts data from the JSON file.

        Returns:
            list: A list of dictionaries containing blog information.

        Raises:
            JSONDecodeError: If the JSON file format is invalid.
    """

    try:
        with open(PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error: The JSON file could not be decoded. Please check the file format.")
        return []
    except FileNotFoundError:
        print(f"Error: File '{PATH}' not found. Returning empty list.")
        return []


def save_posts(blog_posts):
    """
        Saves blog posts data to the JSON file.

        Args:
            blog_posts (list): List of posts data to save.

        Raises:
            IOError: If there is an error writing to the file.
    """
    try:
        with open(PATH, "w", encoding="utf-8") as file:
            json.dump(blog_posts, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error: Unable to write to the file '{PATH}'. Details: {e}")


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = get_posts()
        if blog_posts:
            post_id = blog_posts[-1]['id'] + 1
        else:
            post_id = 1
        post = {'id': post_id,
                'author': request.form.get('author'),
                'title': request.form.get('title'),
                'content': request.form.get('content'),
                }
        blog_posts.append(post)
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template("add.html")


@app.route('/')
def index():
    blog_posts = get_posts()
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
