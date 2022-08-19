from flask import Flask, request, redirect, url_for, flash, jsonify, abort, Response
from flask_cors import CORS
import warnings
import os

warnings.filterwarnings("ignore")

app = Flask(__name__)

CORS(app) #Prevents CORS errors

url_prefix = os.getenv('baseUrl')

@app.route('/', methods=['POST','GET'])
def default_route():

	return 'works!'

@app.route('/'+url_prefix+'/', methods=['POST','GET'])
def default_baseURL():

	return 'works!'
# importing other classes
import serve_models
        
if __name__ == '__main__':
    app.run(host='0.0.0.0')