from fastapi import FastAPI, Query,  Body, Path, APIRouter
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["hotels"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "Radisson", "price": 100},
    {"id": 2, "title": "Дубай", "name": "Burj Al Arab", "price": 200},
    {"id": 3, "title": "Москва", "name": "Метрополь", "price": 150},
    {"id": 4, "title": "Санкт-Петербург", "name": "Астория", "price": 250},
    {"id": 5, "title": "Париж", "name": "Ritz", "price": 300},
    {"id": 6, "title": "Лондон", "name": "Ritz", "price": 300},
    {"id": 7, "title": "Милан", "name": "Ritz", "price": 300},
    {"id": 8, "title": "Барселона", "name": "Ritz", "price": 300},
    {"id": 9, "title": "Мадрид", "name": "Ritz", "price": 300},
    {"id": 10, "title": "Берлин", "name": "Ritz", "price": 300}
]


@router.get("/")
def func():
    return "Hello, World!"

@router.get("", summary="Получение списка отелей")
def get_hotels(
    title: str = None,
    page: int = Query(1, description="Номер страницы", ge=1),
    per_page: int = Query(10, description="Количество отелей на странице", gt=1, lt=30)
):  
    hotels_ = []
    for hotel in hotels:
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
        
    if page and per_page:
        start = per_page * (page - 1)
        end = start + per_page
        return hotels_[start:end]
    return hotels_
    
@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(
        hotel_id: int
    ):
    for i in range(len(hotels)):
        if hotels[i]["id"] == hotel_id:
            return hotels.pop(i)
    return {"error": "Hotel not found"}

''' 
Другой способ удаления отеля
@app.delete("/hotels/{hotel_id}", summary="Удаление отеля")
def delete_hotel(
        hotel_id: int
    ):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotels.remove(hotel)
            return hotel
    return {"error": "Hotel not found"}
    
def delete_hotel(
        hotel_id: int
    ):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}
'''

@router.post("", summary="Добавление отеля")
def add_hotel(
    hotel_data: Hotel
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })


@router.put("/{hotel_id}", summary="Изменение отеля")
def update_hotel(
    hotel_id: int,
    hotel_data: Hotel
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}

@router.patch("/{hotel_id}", summary="Частичное изменение отеля")
def partial_update_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}