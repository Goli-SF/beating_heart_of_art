from fastapi import FastAPI

app = FastAPI()

@app.get("/recommend")
def dummy():
    return{
        'Message' : 'This is supposed to return the N most similar images'
    }


@app.get("/")
def root():
    return {
        'Message': '❤️ Welcome to the beating ❤️ of art ❤️ '
        }
