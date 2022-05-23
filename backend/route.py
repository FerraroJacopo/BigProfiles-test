from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import random
import asyncio

from database import (
    add_data,
    retrieve_datas,

)
from model import (
    ResponseModel,
    DataSchema
)

router = APIRouter()

@router.post("/ingestion", response_description="Data added into the database")
async def add__data(data: DataSchema = Body(...)):
    n = random.uniform(0.01,0.05)
    await asyncio.sleep(n)
    chance = random.randint(1, 100)
    response_code = 200
    if chance <= 10:
        response_code = 500
    data = jsonable_encoder(data)
    new_data = await add_data(n,response_code,data)
    return ResponseModel(new_data, [], "Ingestion complete", response_code)


@router.get("/retrieve", response_description="Data retrieved")
async def get_data(date_from:str, date_to:str):
    datas,metrics = await retrieve_datas(date_from,date_to)
    if datas and metrics:
        return ResponseModel(datas, metrics, "Data retrieved successfully")
    return ResponseModel(datas, metrics, "Missed some data")