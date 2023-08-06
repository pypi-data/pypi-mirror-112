"""
This file is for space news and other scarpping
"""
import requests

# Exceptions
class NoDataAvaliableOnNasa(Exception):
    """
    This error will be raised if there is not data avaliable from nasa
    """

def summary(Body):
    name = str(Body)
    url = "https://hubblesite.org/api/v3/glossary/" + str(name)
    r = requests.get(url)
    Data = r.json()
    if len(Data) != 0:
        retur = Data['definition']
        return retur
    else:
        raise NoDataAvaliableOnNasa("The data you have searched on nasa is not avaliable!")
