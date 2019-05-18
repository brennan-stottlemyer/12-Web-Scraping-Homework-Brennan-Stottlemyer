from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route('/')
def home():
    mars_info = mongo.db.scraped_data.find_one()
    return render_template("index.html", mars_info=mars_info)

@app.route('/scrape')
def scrape():
    mars_info = mongo.db.scraped_data
    mars_data = scrape_mars.scrape()
    mars_info.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)