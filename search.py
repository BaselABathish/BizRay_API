from helper.client import create_client
from datetime import date
import os

def search():
    client = create_client()

    # Ensure output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Call SUCHEFIRMA
    #SUCHFIRMA finds the ids of companies with the name FIRMENWORTLAUT
    suche_params = {
        "FIRMENWORTLAUT": "Signa Prime",
        "EXAKTESUCHE": True, #we can change this later
        "SUCHBEREICH": 1, #Location of the search, I'm not sure what the maximum is
        "GERICHT": "",
        "RECHTSFORM": "",
        "RECHTSEIGENSCHAFT": "",
        "ORTNR": ""
    }

    suche_response = client.service.SUCHEFIRMA(**suche_params)
    ergebnisse = suche_response.ERGEBNIS #this is a list with the information needed for AUSZUG_V2_

    print(f"Found {len(ergebnisse)} companies for 'Signa Prime'")
    print(ergebnisse[0])
    print(type(suche_response))

    # Step 2: Iterate and call AUSZUG_V2_
    for ergebnis in ergebnisse:
        fnr = ergebnis.FNR
        name = ergebnis.NAME[0]
        stichtag = date.today().isoformat()
        umfang = "Kurzinformation"

        print(f"\n🔍 Requesting AUSZUG_V2_ for: {name} (FNR: {fnr})")

        auszug_params = {
            "FNR": fnr,
            "STICHTAG": stichtag,
            "UMFANG": umfang
        }

        try:
            auszug_response = client.service.AUSZUG_V2_(**auszug_params)

            # Create a safe filename
            safe_name = name.replace(" ", "_").replace("/", "_")
            filename = f"{fnr}_{safe_name}.txt"
            filepath = os.path.join(output_dir, filename)

            # Save response to file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(str(auszug_response))

            print(f"✅ Saved to {filepath}")

        except Exception as e:
            print(f"❌ Error for FNR {fnr}: {e}")

if __name__ == "__main__":
    search()
