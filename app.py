import json
from flask import Flask, render_template, request, redirect, abort
from data import PATH

app = Flask(__name__)


def load_posts() -> list[dict]:
    """
    Loads blog posts data from a JSON file and returns it as a sorted list.
    Returns:
         list: A sorted list of blog posts (dictionaries).
               If an error occurs, an empty list is returned.
    Raises:
        JSONDecodeError: If the JSON file format is invalid and cannot be decoded.
        FileNotFoundError: If the specified JSON file is not found.
    """
    try:
        with open(PATH, "r", encoding="utf-8") as file:
            return sorted(json.load(file), key=lambda x: x['id'])
    except json.JSONDecodeError:
        print("Error: The JSON file could not be decoded. Please check the file format.")
        return []
    except FileNotFoundError:
        print(f"Error: File '{PATH}' not found. Returning empty list.")
        return []


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


@app.route('/like/<int:post_id>')
def add_like(post_id):
    """
        Increments the like count for a specific blog post.

        Args:
            post_id (int): The ID of the post to like.
        Returns:
        A redirect to the home page, displaying the updated list of posts.
    """
    post = get_post_by_id(post_id)
    if post is None:
        abort(404, description=f"Post with ID [{post_id}] not found.")

    post['likes'] = post.get('likes', 0) + 1
    save_posts()
    return redirect('/')


@app.route('/delete/<int:post_id>')
def delete(post_id):
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
    abort(404, description=f"Error: Post with ID [{post_id}] does not exist.")


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
        Handles updating an existing blog post.

        Args:
            post_id (int): The ID of the post to update.

        Returns:
            If POST: Redirects to the home page after updating the post.
            If GET: Renders the update post form with the post details.
            If post is not found: Returns a 404 error.
    """
    post = get_post_by_id(post_id)
    if post is None:
        abort(404, description=f"Error: Post with ID [{post_id}] does not exist.")
    if request.method == 'POST':
        post['author'] = request.form.get('author', post['author'])
        post['title'] = request.form.get('title', post['title'])
        post['content'] = request.form.get('content', post['content'])
        save_posts()
        return redirect('/')
    return render_template('update.html', post=post)


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
    blog_posts = load_posts()
    app.run(host="0.0.0.0", port=5000, debug=True)
