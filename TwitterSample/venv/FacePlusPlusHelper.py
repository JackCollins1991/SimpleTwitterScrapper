import requests
from AppData import AppData
import ast

# FacePlusPlus class makes http requests to the Face++ API and returns the results from the face recognition.

class FacePlusPlus():
    def getAttributes(url):

        files = {
            'api_key': (None, AppData.faceapikey),
            'api_secret': (None, AppData.faceapisecret),
            'image_url': (None, url),
            'return_landmark': (None, '1'),
            'return_attributes': (None, 'gender,age,ethnicity'),
        }
        response = requests.post('https://api-us.faceplusplus.com/facepp/v3/detect', files=files)

        # respone is byte string, must parse to dictionary
        str = response.content.decode("UTF-8")
        dict = ast.literal_eval(str)
        result = {}
        try:
            result = dict.get("faces")[0].get("attributes")
        except:
            result = {}
        return result
