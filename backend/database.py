import motor.motor_asyncio
from datetime import datetime
from datetime import timedelta

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongo:27017')
database = client.datas
data_collection = database.get_collection("data_collection")

# helpers
def data_helper(data) -> dict:
    return {
        "id": str(data["_id"]),
        "key": data["key"],
        "payload": data["payload"],
        "creation_datetime": data["creation_datetime"],
        "response_time": data["response_time"],
        "response_code": data["response_code"]
    }

def metrics_helper(data) -> dict:
    return {
        "key": data["_id"]['key'],
        "creation_datetime": data['_id']['creation_datetime'],
        "total_response_time": data["total_response_time"],
        "total_requests": data["total_requests"],
        "total_errors": data["total_errors"]
    }

# Retrieve all datas present in the database
async def retrieve_datas(date_from, date_to):
    if '.' in date_from:
        start = datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S.%fZ")
    else:
        start = datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")

    if '.' in date_to:
        end = datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S.%fZ")
    else:
        end = datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")

    end = end + timedelta(minutes=1)

    query = {
        'creation_datetime':
            {
                '$gte': start,
                '$lt': end,
            }
    }

    aggregation = [
        {
            '$match':
                {
                    'creation_datetime': {
                        '$gte': start,
                        '$lt': end
                    }
                }
        },
        {
            '$group': {
                "_id": {
                    "key": "$key",
                    'creation_datetime': {
                        '$dateToString': {'format': "%Y-%m-%dT%H-%M", 'date': "$creation_datetime"}
                    }
                },
                'total_requests': {
                    '$sum': 1
                },
                "total_response_time": {
                    '$sum': "$response_time"
                },
                "total_errors": {
                    '$sum': {
                        '$cond': [
                            {
                                '$eq':
                                    [
                                        '$response_code', 200
                                    ]
                            },
                            '$sum', 1
                        ]
                    }
                },
            }
        },
        {
            '$sort':
                {
                    '_id.creation_datetime': 1,
                    '_id.key': 1,
                }
        },
    ]

    tmp = []
    metrics = []
    datas = []

    async for data in data_collection.find(query).sort("creation_datetime", -1).limit(10):
        tmp.append(data_helper(data))
    async for metric in data_collection.aggregate(aggregation):
        metrics.append(metrics_helper(metric))
    if len(tmp) > 0:
        creation_datetime_key = tmp[0]['creation_datetime'].strftime("%Y-%m-%d %H:%M")
        for data in tmp:
            if data['creation_datetime'].strftime("%Y-%m-%d %H:%M") == creation_datetime_key:
                datas.append(data)

    return datas, metrics

# Add a new data into to the database
async def add_data(n, response_code, data_data: dict) -> dict:
    data_data['response_time'] = round(n * 1000)
    data_data['response_code'] = response_code
    data_data['creation_datetime'] = datetime.now()
    data = await data_collection.insert_one(data_data)
    new_data = await data_collection.find_one({"_id": data.inserted_id})

    return data_helper(new_data)