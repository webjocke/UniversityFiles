#!/usr/bin/env python3
# ­*­ coding: utf­8 ­*­

# Imports alla the required modules
import json, os, operator

# Loading the file and returns it if found else returns None
def load(file_json):

        """
                Loads the specified file and returns it if found else returns None
        """

        try:
                with open (file_json, encoding='utf-8') as f:
                        data_json = json.load(f)
                        return data_json
        except OSError as err:
                return None

# Returns amout of project in the database
def get_project_count(db):

        """
                Returns the amount of project in the databas
        """

        return len(db)

# Returns the project with the selected ID
def get_project(db, id):

        """
                Returns the project with the selected ID.
        """
   
        for project in db:
                if project["project_id"] == id:
                        return project
        return None


# Seaches in database
def search(db, sort_by='start_date', sort_order='desc', techniques=None, search=None, search_fields=None):

        """
                Handeling a search request.
                Creates a empty templist.
                Filters out all projects that has the right seach text in the right searchfields.
                Filters out all projects with the right techniquies.
                Then comes some code for selecting order.
                Sortes the projects left.
                Returns the projects that passed thought the filters.
        """

        projects_left = []

        projects_left = search_search_fields(db,projects_left,search_fields,search)

        projects_left = search_techniques(projects_left,techniques)

        # Selects the order for the sort function
        if sort_order == 'desc':
                order = True
        elif sort_order == 'asc':
                order = False
        else: # If wrong input in 'sort order'! sorted by desc
                order = True
        if sort_by == None:
                sort_by = 'start_date'

        projects_left.sort(key=operator.itemgetter(sort_by),reverse=order)

        return projects_left


# Selects in all fields in database that the user wants
def search_search_fields(db,projects_left,search_fields,search):

        """
                Checks if the searchs something in the search fields. Used the search_in_search function.
        """

        for project in db:
                if search_fields != None:
                        for item in search_fields:
                                if item in project:

                                        search_in_search(projects_left,search_fields,search,item,project)                                              
                else:
                        for item in project:
                                search_in_search(projects_left,search_fields,search,item,project)
        return projects_left


# Checks if search is none, return all projects, else compare with the search keywork in search_search
def search_in_search(projects_left,search_fields,search,item,project):

        """     
                Checks if the search text is in the selected fields. Used the search_search function for help.
        """

        if search != None:
                if search_search(project[item],search):
                        if get_project(projects_left, project["project_id"]) == None:
                                projects_left.append(project)
        else:
                if get_project(projects_left, project["project_id"]) == None:
                        projects_left.append(project)

        return projects_left  


# Checks if what the user searched for in the selected fields in the database
def search_search(value,search):

        """
                Returns true of false if a specific spot in the search text matches any text in the search field.
        """

        if str(search).lower() in str(value).lower() :
                return True
        else:
                return False 

                
# Filters out the project that uses a specific techquies
def search_techniques(projects_left, tech):

        """
                Filters out the project that uses a specific techquies
        """

        # If not techquines selected, return all as is
        if tech == None or tech == []:
                print("hej")
                return projects_left

        # Filter the projects
        temp = []
        for project in projects_left:
                if set(project['techniques_used']).issuperset(tech):
                        temp.append(project)
        return temp





# Gets a list of all projects for the database
def get_techniques(db):

        """
                Returns a sorted list of all tecniques
        """

        all_techniques = []
        for project in db:
                for technique in  project["techniques_used"]:
                        if technique not in all_techniques:
                                all_techniques.append(technique)

        all_techniques.sort()

        return all_techniques


# Returns a list of all techqniues and its projects (id and name)
def get_technique_stats(db):

        """
                Returns a custom list with techniques and its projects.
        """

        tech_status = {}

        for tech in get_techniques(db):

                tech_status[tech] = []
           
                for project in db:
                        if tech in project["techniques_used"]:
                                temp_dir ={"id": project["project_id"], "name": project["project_name"]}
                                tech_status[tech].append(temp_dir)
                 
        return tech_status
