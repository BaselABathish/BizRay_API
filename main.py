from fastapi import FastAPI
import requests
from client import create_client

from search import search

app = FastAPI()
client = create_client()


@app.get('/')
def confirm_connection():
    return {"Status": "Active"}

@app.get("/search/{company_name}")
def search_companies(company_name: str):
    r = search(company_name)
    print(type(r))
    return {"Results": r}





#fixed