from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import modules.common.routes
import modules.stronghold.routes

origins = [
    "http://localhost:9000",
    "http://localhost:3000",
]

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(modules.common.routes.router)
app.include_router(modules.stronghold.routes.router)


@app.get('/')
async def index():
    return 'ok'


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=3000, reload=True)
