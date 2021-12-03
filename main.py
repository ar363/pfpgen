from fastapi import FastAPI
import json

app = FastAPI()

with open('colors.json') as f:
    colors = json.loads(f.read())

@app.get('/')
def get_pfp():
    return {'colors': colors}