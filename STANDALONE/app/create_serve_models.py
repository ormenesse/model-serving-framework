import os
import time
import glob

baseUrl = os.getenv('baseUrl')
gitUserName = os.getenv('usergit')
gitPassword = os.getenv('password')
gitPath = os.getenv('gitPath').replace('https://','')

# update git
cmd = "rm -rf models_serve/ && git clone https://{}:{}@{} ./models_serve".format(gitUserName,gitPassword,gitPath)
os.system(cmd)
time.sleep(2)

# creating serve_models.py
writeImports="""import flask
import pandas as pd
import numpy as np
import warnings
import json
import gc
import os

from __main__ import app

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

@app.route('/{}/refactor',methods=['GET'])
def refactor():
    gc.collect()
    cmd = "cd /app/app/ && python3 create_serve_models.py"
    os.system(cmd)
    
    return True

\n""".format(baseUrl,'{}')

runSepareteModel = """
#
@app.route('/{}/{}', methods=['POST'])
def score_{}():
    gc.collect()
    variables = pd.json_normalize(flask.request.json['variables'])
    scorer = {}.transform_predict('{}')
    _dic_ = json.loads(json.dumps(scorer.transform_predict(variables.copy()),cls=NpEncoder))
    del scorer
    return _dic_
"""

# Last and Most Important Method
runAllModels = """
#
@app.route('/{}/all', methods=['POST'])
def score_all():
    gc.collect()
    _dic_ = {}
    variables = pd.json_normalize(flask.request.json['variables'])
""".format(baseUrl,'{}')

addToRunAllModels = """
    scorer = {}.transform_predict('{}')
    _dic_.update(json.loads(json.dumps(scorer.transform_predict(variables.copy()),cls=NpEncoder)))
"""
finalAddToRunAllModels = """
    del scorer
    return _dic_
"""

with open('serve_models.py','w') as f:
    arrayMethods = []
    f.write(writeImports)
    for _path in glob.glob('./models_serve/*'):
        nameClass = _path.split('/')[-1]
        f.write('from models_serve.{} import etls as {}\n'.format(nameClass,nameClass))
        arrayMethods.append(runSepareteModel.format(baseUrl,nameClass,nameClass,nameClass,_path+'/'))
        runAllModels = runAllModels + addToRunAllModels.format(nameClass,_path+'/')
    runAllModels = runAllModels + finalAddToRunAllModels
    f.write('warnings.filterwarnings("ignore")\n')
    f.write('\n'.join(arrayMethods))
    f.write(runAllModels)
    
cmd = "/usr/bin/supervisord"
os.system(cmd)
cmd = "supervisorctl restart gunicorn"
os.system(cmd)
print("Daemon Restarted! All Done!")
time.sleep(2)
