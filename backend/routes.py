from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################


@app.route("/picture", methods=["GET"])
def get_pictures():
    """Fetches pictures from global data variable.
    """
    # Return JSON response with the loaded data
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Fetches picture from global data varaiable by ID
    Handles case for ID not found in data
    """
    for picture in data:
        if picture.get("id") == id: 
            return jsonify(picture), 200
    return {"Message": f"Picture with id: {id} cannot be found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Appends new picture JSON data to global data list from request obj
    Handles cases for bad JSON data or duplicate picture id
    """
    picture_data = request.json
    if picture_data is None:
        return {"Message": "Invalid JSON data"}, 404
    
    # Check if the picture ID already exists in the pictures list
    picture_id = picture_data.get("id")
    if any(picture.get("id") == picture_id for picture in data):
        return {"Message": f"picture with id {picture_id} already present"}, 302
    
    data.append(picture_data)
    return jsonify(picture_data), 201

  
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Fetches a picture from data by id and updates picture json data
    """
    update_data = request.json
    for picture in data:
        if picture.get("id") == id: 
            picture.update(update_data)
            return jsonify (picture), 200
    return {"Message": "Picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Fetches a picture from data list by id and deletes 
    """
    for picture in data:
        if picture.get("id") == id:
            data.remove(picture)
            return jsonify(picture), 204
    return {"Message": "Picture not found"}, 404