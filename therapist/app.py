from flask import Flask
from flask_restful import Api
from therapist.therapist_resources import TherapistDiscovery

app=Flask(__name__)

api=Api(app)


@app.route("/")
def home():
    return "<h1 style='color:blue'>This is the Therapist Details  pipeline!</h1>"


api.add_resource(TherapistDiscovery, '/therapist_details')
