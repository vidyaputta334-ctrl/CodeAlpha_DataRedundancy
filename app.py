from flask import Flask, request
import sqlite3

app = Flask(__name__)


def create_database():
    connection = sqlite3.connect("database.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)

    connection.close()


create_database()


@app.route("/", methods=["GET", "POST"])
def home():

    message = ""

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]

        connection = sqlite3.connect("database.db")

        try:
            connection.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (name, email)
            )

            connection.commit()
            message = "Data added successfully!"

        except sqlite3.IntegrityError:
            message = "Duplicate data! This email already exists."

        connection.close()

    connection = sqlite3.connect("database.db")

    users = connection.execute(
        "SELECT id, name, email FROM users"
    ).fetchall()

    connection.close()

    table = ""

    for user in users:
        table += f"""
        <tr>
            <td>{user[0]}</td>
            <td>{user[1]}</td>
            <td>{user[2]}</td>
            <td>
                <a href="/delete/{user[0]}">Delete</a>
            </td>
        </tr>
        """

    return f"""
    <html>

    <head>
        <title>Data Redundancy Removal System</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>

    <body>

        <div class="container">

            <h1>Data Redundancy Removal System</h1>

            <form method="POST">

                <label>Name:</label>
                <input type="text" name="name" required>

                <br><br>

                <label>Email:</label>
                <input type="email" name="email" required>

                <br><br>

                <button type="submit">Add Data</button>

            </form>

            <h3>{message}</h3>

            <h2>Stored Unique Data</h2>

            <table>

                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Action</th>
                </tr>

                {table}

            </table>

        </div>

    </body>

    </html>
    """


@app.route("/delete/<int:user_id>")
def delete(user_id):

    connection = sqlite3.connect("database.db")

    connection.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    connection.commit()
    connection.close()

    return """
    <script>
        window.location.href = "/";
    </script>
    """


if __name__ == "__main__":
    app.run(debug=True)