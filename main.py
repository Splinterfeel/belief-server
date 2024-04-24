from fastapi import FastAPI
import uvicorn
import modules.common.routes


app = FastAPI(debug=True)
app.include_router(modules.common.routes.router)


@app.get('/')
async def index():
    return 'ok'


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=3000, reload=True)
