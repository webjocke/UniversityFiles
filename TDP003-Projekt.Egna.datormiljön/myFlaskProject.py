#!/usr/bin/env python3
# ­*­ coding: utf­8 ­*­

# Flask import and start-code
from flask import Flask, request, render_template
app = Flask(__name__,static_url_path='/static')

# Importing requierd modules
import data
import json


# Front Page
@app.route("/")
def hello():
    """
        Handling requests for the index page. Returns a html page with some css.
        This function loads the all data thoguht the API and uses the search-function of the API to filter out the latest projects.
        Uses the ninja function render_template to combine the filtered project with the html-page
    """

    db = data.load("data.json")
    projects = data.search(db)

    return render_template("index.html", projects=projects)

# List all techniques Page
@app.route("/technologies")
def techniques():
    """
        Handling requests for the technologies page. Returns a html page with some css.
        This function loads the all data thoguht the API and uses the get_technique_stats-function of the API that returns all project stats for the tech page.
        Uses the ninja function render_template to combine the tech-data with the html-page
    """

    db = data.load("data.json")
    projects = data.get_technique_stats(db)
    return render_template("technologies.html", projects=projects)


# List all project Page
@app.route("/list", methods=["POST", "GET"])
def list():
    """
        Handling requests for the list page. Returns a html page with some css. Uses the methods GET.
        This function loads the all data thoguht the API and uses the get_techniques-function of the API that returns a list of all techniques for the checkboxes on the page.
        Then it pushes the data the API:s search-function.
        Also have some selfexplanitory code for autofilling the page on load.
        Uses the ninja function render_template to combine the data with the html-page
    """

    db = data.load("data.json")
    all_techs = data.get_techniques(db)
    # Check if the user has submited the form
        # If the user selected a techique

    all_projs = data.search(db, request.args.get("order_list"), request.args.get("list_order"), request.args.getlist("filter_tech"),request.args.get("search_box"))
            
    # Save the last search form text
    if request.args.get("search_box") == None:
        search_temp = ''
    else: 
        search_temp = request.args.get("search_box")
        
    if request.args.get("order_list") == None:
        order_box = ''
    else: 
        order_box = request.args.get("order_list")
        
    # Does stuff, need to be here to work, tried without multiply times, no luck
    return render_template("list.html", projects=all_projs, techs=all_techs, search_nu=search_temp,order_box=order_box)


# Specific Project Page
@app.route("/project/<int:xid>")
def project(xid):

    """
        Handling requests for the project page. Returns a html page with some css. This function uses the id-number form the URL request.
        This function loads the all data thoguht the API and uses the get_project-function of the API that returns the required project.
        Uses the ninja function render_template to combine the data with the html-page
        Also has some error handling for is the types a unexpected id in the URL, the it renders the error page instead of the regular page.
    """

    db = data.load("data.json")
    project = data.get_project(db,xid)
    if project == None:
        return render_template("error.html", titel="Error 404", text="ID:t finns inte! Försök igen!")
    else:
        return render_template("project.html", project=project)

@app.errorhandler(404)
def error(e):

    """
        Handling error requests.
        Uses the ninja function render_template to combine the data with the html-page
    """

    #return repr(e)
    return render_template("error.html", titel="Error 404", text="Sidan du sökte hittades inte, vänligen testa igen.")


# Start flask app if the file is run as the main-file instead of as a module
if __name__ == "__main__":
    app.run(debug=False)

# Enable logging into logfile.log, but 
if not app.debug:
    import logging
    logging.basicConfig(filename="logfile.log", level=logging.INFO)
