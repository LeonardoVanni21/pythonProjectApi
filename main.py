from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from starlette.responses import HTMLResponse


class Car(BaseModel):
    id: int
    name: str
    model: str
    year: int
    color: str
    price: float


app = FastAPI()

cars = {}

cars[1] = Car(id=1, name="Fuscão Preto", model="Fusca", year=1970, color="Preto", price=10000)
cars[2] = Car(id=2, name="Gol Bolinha", model="Gol", year=1990, color="Vermelho", price=15000)
cars[3] = Car(id=3, name="Fiesta Dos Véio", model="Fiesta", year=2000, color="Azul", price=20000)


@app.post("/cars/")
async def create_car(car: Car):
    if car.id in cars:
        return {"error": "Carro já existe"}
    cars[car.id] = car
    return car


@app.get("/cars/")
async def read_cars():
    return cars


@app.get("/cars/{car_id}")
async def read_car(car_id: int):
    if car_id not in cars:
        return {"error": "Carro inexistente"}
    return cars[car_id]


@app.put("/cars/{car_id}")
async def update_car(car_id: int, car: Car):
    if car_id not in cars:
        return {"error": "Carro inexistente"}
    cars[car_id] = car
    return car


@app.delete("/cars/{car_id}")
async def delete_car(car_id: int):
    if car_id not in cars:
        return {"error": "Carro inexistente"}
    del cars[car_id]
    return {"message": "Carro deletado com sucesso"}


@app.get("/carsHtml/")
async def read_cars_html():
    if len(cars) == 0:
        return HTMLResponse(content=f"<html><body><h1>Nenhum carro encontrado</h1></body></html>", status_code=404)
    html_content = """
    <html>
        <head>
            <title>Carros</title>
        </head>
        <body>
            <h1>Carros</h1>
            <ul>
"""

    for car in cars.values():
        html_content += f"\t\t<li>{car.name} - {car.model} - {car.year} - {car.color} - {car.price}</li>\n"

    # Fim do HTML
    html_content += """
            </ul>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/carsHtml/{car_id}")
async def read_car_html(car_id: int):
    if car_id not in cars:
        return HTMLResponse(content=f"<html><body><h1>Carro não encontrado</h1></body></html>", status_code=404)
    return HTMLResponse(
        content=f"<html><body><h1>{cars[car_id].name} - {cars[car_id].model} - {cars[car_id].year} - {cars[car_id].color} - {cars[car_id].price}</h1></body></html>",
        status_code=200)


client = TestClient(app)

def test_read_car():
    response = client.get("/cars/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Fuscão Preto",
        "model": "Fusca",
        "year": 1970,
        "color": "Preto",
        "price": 10000.0
    }

def test_delete_car():
    response = client.delete("/cars/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Carro deletado com sucesso"}

    response = client.get("/cars/1")
    assert response.status_code == 200
    assert response.json() == {"error": "Carro inexistente"}

