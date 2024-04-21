from fastapi import FastAPI
import uvicorn


app = FastAPI(debug=True)

@app.get('/')
async def index():
    return 'ok'


@app.post('login')
async def login():
    return True


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=3000, reload=True)
