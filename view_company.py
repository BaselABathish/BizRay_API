from client import create_client
from datetime import date
from zeep import helpers #so we can actually do something with the response


def view_company(fnr): #maybe fnr later
    client = create_client()

    timestamp = date.today().isoformat()


    auszug_params = {
        "FNR": fnr,
        "STICHTAG": timestamp,
        "UMFANG": "Kurzinformation"
    }

    try:
        auszug_response = client.service.AUSZUG_V2_(**auszug_params)
        data_dict = helpers.serialize_object(auszug_response)
        return data_dict
    except Exception as e:
        print(e)
        return e





