from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app
app = Flask(__name__)

# # Create connection variable
# conn = 'mongodb://localhost:27017'

# # Pass connection to the pymongo instance.
# client = pymongo.MongoClient(conn)

# # Connect to a database. Will create one if not already available.
# db = client.mars_db


# # Drops collection if available to remove duplicates
# db.mars_data.drop()

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

mongo.db.collection.drop()

@app.route("/")
def home():
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scraper():
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({},mars_data,upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

