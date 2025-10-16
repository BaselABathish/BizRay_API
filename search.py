#This is just basic search functionality to find the name of the companies

from client import create_client
from datetime import date
import os
from zeep import helpers #so we can actually do something with the response

def search(company_name, exact_search = True, search_area = 1):
    client = create_client() #for now

    # Ensure output directory exists WE MIGHT USE THIS LATER???
    #output_dir = "search_results"
    #os.makedirs(output_dir, exist_ok=True)

    #SUCHFIRMA finds the ids of companies with the name like FIRMENWORTLAUT
    suche_params = {
        "FIRMENWORTLAUT": company_name,
        "EXAKTESUCHE": True, #we can change this later
        "SUCHBEREICH": 1, #Location of the search, I'm not sure what the maximum is
        "GERICHT": "",
        "RECHTSFORM": "",
        "RECHTSEIGENSCHAFT": "",
        "ORTNR": ""
    }

    suche_response = client.service.SUCHEFIRMA(**suche_params)
    ergebnisse = suche_response.ERGEBNIS #this is a list with the information needed for AUSZUG_V2_

    print(f"Found {len(ergebnisse)} companies for 'Signa Prime'---------------------------------------------------\n\n\n")
    #print(ergebnisse[0])
    #print(type(suche_response))

    
    results = display_results(client, ergebnisse)
    #print(type(results))

    return results


def display_results(client, ergebnisse):
    results = []
    for ergebnis in ergebnisse:
        fnr = ergebnis.FNR
        name = ergebnis.NAME[0]
        timestamp = date.today().isoformat()
        umfang = "Kurzinformation"

        #print(f"\n🔍 Requesting AUSZUG_V2_ for: {name} (FNR: {fnr})")
    
        auszug_params = {
            "FNR": fnr,
            "STICHTAG": timestamp,
            "UMFANG": umfang
        }


        try:
            auszug_response = client.service.AUSZUG_V2_(**auszug_params)
            data_dict = helpers.serialize_object(auszug_response)
            r = data_dict['FIRMA']['FI_DKZ02'][0]['BEZEICHNUNG'] #this is not optimal
            fnr = data_dict['FNR']
            results.append((r, fnr))
        except Exception as e:
            print(e)
            return e

    #print(type(results))
    return results

if __name__ == "__main__":
    search('Signa prime')
