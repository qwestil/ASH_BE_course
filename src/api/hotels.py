from fastapi import FastAPI, Query,  Body, Path, APIRouter
from sqlalchemy import insert, select
from src.database import async_session_maker
from src.schemas.hotels import Hotel, HotelPATCH
from src.models.hotels import HotelsOrm

router = APIRouter(prefix="/hotels", tags=["hotels"])

@router.get("/")
def func():
    return "Hello, World!"

@router.get("", summary="Получение списка отелей")
async def get_hotels(
    id: int = None,
    title: str = None,
    page: int = Query(1, description="Номер страницы", ge=1),
    per_page: int = Query(10, description="Количество отелей на странице", gt=1, lt=30)
):  
    
    limit = per_page
    offset = per_page * (page - 1)
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if id:
            query = query.filter_by(id=id)
        if title:
            query = query.filter.by(title=title)
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        
        result = await session.execute(query)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        
        hotels = result.scalars().all()
        # print(type(hotels), hotels)
        return hotels
        
    
    # hotels_ = []
    # for hotel in hotels:
    #     if title and hotel["title"] != title:
    #         continue
    #     hotels_.append(hotel)
        
    # if page and per_page:
    #     start = per_page * (page - 1)
    #     end = start + per_page
    #     return hotels_[start:end]
    # return hotels_
    
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
async def add_hotel(
    hotel_data: Hotel
):
    async with async_session_maker() as session:
        add_hotel_stmnt = insert(HotelsOrm).values(**hotel_data. model_dump())
        print(add_hotel_stmnt.compile(compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmnt)
        await session.commit()
        
    return {"status": "OK"}


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