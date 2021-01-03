from datetime import datetime
from flask import make_response, abort, jsonify
from db_utils import add, list_stories, get, update 
import connexion
from jsonschema import validate, ValidationError, SchemaError
import readtime
from spellchecker import SpellChecker
import json


schema = {
    'type': 'object',
    'properties': {
        'body': {'type': 'string', 'message': {'required': "BODY REQ"} },
        'description': {'type': 'string', 'message': {'required': "DESCR "} },
        'title': {'type': 'string', 'message': {'required': "TITLE REQ"} }
    },
    'required': ['body', 'description', 'title']
}

app = connexion.App(__name__, specification_dir="./")


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return {'hours':hour, 'mins': minutes, 'secs':seconds}

def read_all(length=5, offset=0):
    """
    This function responds to a request for /api/strory
    with the complete lists of story

    :return:        list of story
    """
    # length = param.get("length", None)
    # offset = param.get("offset", None)

    story_array = []
    stories   =   list_stories(length, offset)
    for story in stories:
        story_obj   =   {
                            "id": story['id'],
                            "title": story['title'], 
                            "description": story['description'],
                            "body": story['body'],
                            "tags": story['tags'],
                            "createdAt": story['created'],
                            "published": story['published']
                        }
        story_array.append(story_obj)                
    
    return {
        "QueryResponse": {"startPosition": offset, "stories": story_array}
    }, 200


def read_one(id):

    """
    This function responds to a request for /api/story/{id}
    with one matching blog from story

    :param lname:   id of story to find
    :return:        story matching id
    """

    story = get(id)

    # Does the story exist?
    if story:
        readtime_result = readtime.of_html(story['body'])
        return {
            "id": story['id'],
            "title": story['title'], 
            "description": story['description'],
            "body": story['body'],
            "timeToRead": convert(readtime_result.seconds),
            "tags": story['tags'],
            "createdAt": story['created'],
            "published": story['published']
        }
    else:
        abort(404, "Record not found")

@app.route('/story', methods=['POST'])
def create(story):
    try:
        validate(story, schema)
    except ValidationError as e:
        abort(400,e.message,)

    title = story.get("title", None)
    description = story.get("description", None)
    body = story.get("body", None)
    tags = story.get("tags", None)
    story_id = add(title,description,body,tags)

    return read_one(story_id), 201


def publish(id):

    """
    This function updates an existing story 

    :param id:   id of person to update in the story status
    :return:        updated story 
    """
    story = get(id)
    if story:
        update(id,True)
        return read_one(id)
    else:
        abort(404, "Record not found")

def unpublish(id):

    """
    This function updates an existing story 

    :param id:   id of person to update in the story status
    :return:        updated story 
    """
    story = get(id)
    if story:
        update(id,False)
        return read_one(id)
    else:
        abort(404, "Record not found")

def spellchecker(id):

    story = get(id)
    if story:
        spell = SpellChecker()
        misspelled = spell.unknown(story['body'].split(" "))
        if len(misspelled)>0:
            return {'misspelledWords': list(misspelled)}, 200
        else:
            return {'misspelledWords': []}, 200
    else:
        abort(404, "Record not found")
