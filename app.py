import json
from flask import Flask, render_template, request, redirect, abort
from data import PATH

app = Flask(__name__)

# Global variable to store the blog posts data
blog_posts = []


def load_posts() -> None:
    """
    Loads blog posts data from the JSON file into the global `blog_posts` variable.

    Raises:
        JSONDecodeError: If the JSON file format is invalid.
    """
    global blog_posts
    try:
        with open(PATH, "r", encoding="utf-8") as file:
            blog_posts = sorted(json.load(file), key=lambda x: x['id'])
    except json.JSONDecodeError:
        print("Error: The JSON file could not be decoded. Please check the file format.")
        blog_posts = []
    except FileNotFoundError:
        print(f"Error: File '{PATH}' not found. Returning empty list.")
        blog_posts = []


def get_post_by_id(post_id: int) -> dict | None:
    """
    Retrieves a post by its ID.

    Args:
        post_id (int): The ID of the post to retrieve.

    Returns:
        dict | None: The post data if found, otherwise None.
    """
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


def save_posts() -> None:
    """
    Saves blog posts data from the global `blog_posts` variable to the JSON file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    try:
        with open(PATH, "w", encoding="utf-8") as file:
            json.dump(blog_posts, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error: Unable to write to the file '{PATH}'. Details: {e}")


@app.route('/delete/<int:post_id>')
def delete(post_id: int):
    """
    Deletes a post by its ID.

    Args:
        post_id (int): The ID of the post to delete.

    Returns:
        Redirects to the home page if successful, or a 404 error if the post does not exist.
    """
    post = get_post_by_id(post_id)
    if post:
        blog_posts.remove(post)
        save_posts()  # Save updated data to file
        return redirect('/')
    else:
        abort(404, description=f"Error: Post with ID [{post_id}] does not exist.")


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handles the addition of a new blog post.

    Returns:
        If POST, adds the post and redirects to the home page.
        If GET, renders the add post form.
    """
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        if not all([author, title, content]):
            return "Error: All fields are required!", 400

        post_id = (blog_posts[-1]['id'] + 1) if blog_posts else 1

        post = {
            'id': post_id,
            'author': author,
            'title': title,
            'content': content,
        }
        blog_posts.append(post)
        save_posts()  # Save updated data to file
        return redirect('/')

    return render_template("add.html")


@app.route('/')
def index():
    """
    Renders the home page with a list of blog posts.

    Returns:
        Renders the index page with the blog posts.
    """
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    load_posts()  # Load posts once at startup
    app.run(host="0.0.0.0", port=5000, debug=True)
