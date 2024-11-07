import json
from flask import Flask, render_template
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

    
@app.route('/')
def index():
    blog_posts = get_posts()
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

