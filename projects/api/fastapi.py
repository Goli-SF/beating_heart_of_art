from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.recommend("/")

@app.get("/")
def root():
    return {
        'Message': '❤️ Welcome to the beating ❤️ of art ❤️ '
        }
