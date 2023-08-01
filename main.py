import flask
import json
import os
from flask import send_from_directory, request
import openai
import pinecone

openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = "sk- . . ."

PINECONE_API_KEY = "c47d17e1-62da-4f4a-a319-9608e3104d13"
# MT PINECONE_API_KEY = "a2a86279-ffc8-490c-9365-0d3d32a458a5"

YOUR_ENV = "us-west1-gcp-free"
# MT YOUR_ENV = "us-west4-gcp"

index_name = "chat-doc-ts"

namespace_name = "mb"

# Flask app should start in global layout
app = flask.Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.png')

@app.route('/')

@app.route('/home')
def home():
    return "Hello World"

def complete_xq(query):

    # openai.api_key = "sk- . . ."

    # initializing a Pinecone index
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=YOUR_ENV
    )

    index = pinecone.Index(index_name)

    xq = openai.Embedding.create(input=query, engine=MODEL)['data'][0]['embedding']

    res = index.query([xq], top_k=1, include_metadata=True, namespace=namespace_name)
   
    """
    print("\nThe most similar questions:")
    for match in res['matches']:
        print(f"{match['score']:.2f}: {match['metadata']['question']}")
    """
          
    # print("\nAnswer:")    
    for match in res['matches']:
        # print(f"{match['score']:.2f}: {match['metadata']['answer']}\n")
        # print(f"\nURL: {match['metadata']['url']}\n\nTITLE: {match['metadata']['title']}\n\nSPAN: {match['metadata']['span']}\n\nDIV: {match['metadata']['div']}\n")
        query = f"\nURL: {match['metadata']['url']}\n\nTITLE: {match['metadata']['title']}\n\nSPAN: {match['metadata']['span']}\n\nDIV: {match['metadata']['div']}\n"

    return query   


@app.route('/webhook', methods=['GET','POST'])
def webhook():

    # openai.api_key = "sk- . . ."

    # initializing a Pinecone index
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=YOUR_ENV
    )

    index = pinecone.Index(index_name)

    req = request.get_json(force=True)

    query_text = req.get('sessionInfo').get('parameters').get('query_text')

    # query_with_contexts = retrieve(query_text)

    #answer = complete_xq(query_with_contexts)
    answer = complete_xq(query_text)

    res = {
        "fulfillment_response": {"messages": [{"text": {"text": [answer]}}]}
    }

    return res


embed_model = "text-embedding-ada-002"
MODEL = "text-embedding-ada-002"
namespace_name = "mb"

"""
def retrieve(query_text):
    ...

    return prompt
"""

if __name__ == "__main__":

    app.run()
#    app.debug = True