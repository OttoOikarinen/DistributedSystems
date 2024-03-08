import xml.etree.ElementTree as ET
from xmlrpc.server import SimpleXMLRPCServer
import requests

# Function to process client input and save data to XML database
def process_input(topic, text, timestamp):
    # Parse XML file or create a new one if it doesn't exist
    try:
        tree = ET.parse('notebook.xml')
        root = tree.getroot()
    except FileNotFoundError:
        root = ET.Element('notebook')
        tree = ET.ElementTree(root)

    # Check if the topic exists, if not create a new entry
    topic_exists = False
    for note in root.findall('note'):
        if note.attrib['topic'] == topic:
            topic_exists = True
            note_element = note
            break

    if not topic_exists:
        note_element = ET.SubElement(root, 'note')
        note_element.set('topic', topic)

    # Append new note data
    note_data = ET.SubElement(note_element, 'data')
    note_data.set('timestamp', timestamp)
    note_data.text = text

    # Save changes to the XML file
    tree.write('notebook.xml')

    if topic_exists == False:
        return "Topic added succesfully!"
    else:
        return "Topic appended succesfully!"

# Function to make Wikipedia API query
def query_wikipedia(topic):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": topic,
        "format": "json",
        "limit": 1
    }
    response = requests.get(url, params=params)
    # If response is successful:
    if response.status_code == 200:
        data = response.json()
        if data[1]:  # Check that search results are not empty
            return data[3][0]  # Return the URL of the first search result
        else:
            return "No Wikipedia article found for the topic."
    else:
        return "Failed to query Wikipedia API."


# Create an XML-RPC server
try:
    server = SimpleXMLRPCServer(('localhost', 8000))
    print("Server started on localhost:8000...")
    # Register functions to be visible to clients
    server.register_function(process_input, 'process_input')
    server.register_function(query_wikipedia, 'query_wikipedia')

    # Run the server
    server.serve_forever()
    
except Exception:
    print("Creating server failed.")


