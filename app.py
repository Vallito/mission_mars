from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def home():
    # Retrieve the latest data from Mongo 
    mars_data = mongo.db.collection.find_one()
    

    # Render an index.html template and pass it the data from the database
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_info()

    # Get Mongo data 
    mongo.db.collection.update({}, mars_data, upsert=True)

    # render html from templates folder
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)