"""
This file is for space news and other scarpping
"""
import requests

# Exceptions
class NoDataAvaliableOnNasa(Exception):
    """
    This error will be raised if there is not data avaliable from nasa
    """

def SolarBodies(body):
    """
    Returns a dictanary of information of a solar body,
    It gets the data from Nasa.
    """
    url = "https://api.le-systeme-solaire.net/rest/bodies/"
    r = requests.get(url)
    Data = r.json()
    bodies = Data['bodies']
    Number = len(bodies)
    url_2 = "https://api.le-systeme-solaire.net/rest/bodies/" + str(body)
    rrr = requests.get(url_2)
    data_2 = rrr.json()
    mass = data_2['mass']['massValue']
    bolume = data_2['vol']['volValue']
    density = data_2['density']
    gravity = data_2['gravity']
    escape = data_2['escape']
    return {'Number': Number, 'mass': mass, 'gravity': gravity, 'escape_velocity': escape, 'density': density}