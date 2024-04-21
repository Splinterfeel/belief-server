from fastapi import FastAPI
import uvicorn
import time
from schemas.auth import LoginResult


app = FastAPI(debug=True)

@app.get('/')
async def index():
    return 'ok'


@app.post('/login')
async def login() -> LoginResult:
    # time.sleep(2)
    return LoginResult(successful=True, login='test')


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=3000, reload=True)
