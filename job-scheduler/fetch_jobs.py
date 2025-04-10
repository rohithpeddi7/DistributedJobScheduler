import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime
from croniter import croniter
from bson import ObjectId
import time
import os
from kafka import KafkaProducer
from config import *
import json

producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

load_dotenv()

MONGO_CONN_STR = os.getenv("DB_CONN_STR")
MONGO_DB_NAME = os.getenv("DB_NAME")

mongodb_client = AsyncIOMotorClient(MONGO_CONN_STR)
mongodb = mongodb_client[MONGO_DB_NAME]

async def job_fetcher(db):

    while True:

        await asyncio.sleep(50)

        collection = db.scheduled_jobs

        current_time = datetime.now()

        cursor = collection.find({"next_run_at":{"$lte": current_time}}).sort("next_run_at")
        for document in await cursor.to_list():

            doc_to_send = {"job_id": str(document["_id"]), "scheduled_time" : document["next_run_at"].isoformat() + "Z", "dockerfile_url": document["dockerfile_name"]}
            print("Debug: ", doc_to_send)
            producer.send(JOBS_TOPIC, json.dumps(doc_to_send).encode("utf-8"))
            print(document)
            job_id = document["_id"]
            cron_expression = document["cron_expression"]
            if document["is_one_time"]:
                result = await collection.delete_one({"_id": job_id})
                # print(result)
                continue
            next_run_at = croniter(cron_expression, current_time).get_next(datetime)
            result = await collection.replace_one({"_id": job_id}, {**document, "next_run_at":next_run_at})
            print(result)

if __name__=="__main__":

    asyncio.run(job_fetcher(mongodb))


