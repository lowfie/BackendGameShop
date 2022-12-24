from fastapi import FastAPI

app = FastAPI()


@app.get('/', summary='some test')
async def test_get_response():
    return {'result': 'response is work'}
