# model-serving-framework
A kubernetes way to serve automatically your models. No bureaucracy.

This project is inteded to autoserve machine learning models, or any ETL project you may like on the go.
On the docker version, the user must have a github repository with 'n' folders containing 'n' ML Models or ETL's. The container/pod will everyday update it's own code and serve your models automatically.
Each folder in your repository must have a class named as etls.py (extract, transform, load and score) and it must contain 'transform_predict()' method, note that it must return a dict structure.

Structure:
```
-app.py
-serve_models.py (created by create_serve_models.py)
-models_serve (will clone everyday your github repository with your models and ETL's)
    - Model1:
        - etls.py
            __init__()
            transform_predict() -> dict()
            any_others_method_you_may_need()
    - Model2:
        - etls.py
            __init__()
            transform_predict() -> dict()
            any_others_method_you_may_need()
```
The app will automatically serve on port 80 and each model will be wating to be served on, for an exemple:
- /baseUrl/Model1
- /baseUrl/Model2
- /baseUrl/Etl1
- etc...

Thinking on serve all the possible models there is a method implemented to serve all of your models:
- /baseUrl/all
This method will return all of your models into one dict.

Note that thiking kubernetes and nginx ingress, the environment variable 'baseUrl' is needed.

If your model needs any variables, you should call de URL posting a JSON:
```
data= {
    'variables' : {
        'var1' : 1
        'var2' : 'blabla'
        'var3' : 123.90
        etc.
    }
}
```
And the response should be a JSON with the reponse returned by your 'transform_predict()' method. Note that you should handle possible errors in your classes.

Note that this project is not intended to run BATCH scoring strategy, but a row scoring. On a daily basis, you should configure a load balance a set as many parallel pods as possible.

## Docker Version

On requirements.txt you should insert any python libraries you may want use.
When running your docker, you should pass the environment variables displayed in the env file.

## Standlone Version

On requirements.txt you should insert any python libraries you may want use.
When running your docker, you should run the bash file containing environment variables displayed in the env file.
Note that, in the standalone version, all of your models, ETL's should be pasted in the folder models_serve. 
This project contain an example on how your class should be implemented.
