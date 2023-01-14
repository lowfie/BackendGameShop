from fastapi import FastAPI

from app.core.logic.routes.reg_routers import api_router

app = FastAPI()
app.include_router(api_router)


@app.get('/', summary='some test')
async def test_get_response():
    return {'result': 'response is work'}
