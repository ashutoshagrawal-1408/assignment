from flask import render_template
import connexion
import json

# Create the application instance
app = connexion.App(__name__, specification_dir="./")

app.add_api("swagger.yml")
# create a URL route in our application for "/"
@app.route("/")
def home():
    return json.dumps({"message": "Server is running", "link":"<a href='http://localhost:5000/api/ui/#/'>Swagger API Doc</a>"}), 201


if __name__ == "__main__":
    app.run(debug=True)