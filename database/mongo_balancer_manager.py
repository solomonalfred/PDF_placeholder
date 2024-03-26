import motor.motor_asyncio
import pymongo
import os
from constants.balancer_items import *


class LoadBalancerManager:
    def __init__(self, database_name, collection_name):
        # server db URL: "mongodb://mongodb:27017"
        # test db URL: "mongodb://localhost:27017"
        self.client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongodb:27017")
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

        self.sync_client = pymongo.MongoClient("mongodb://mongodb:27017")
        self.sync_database = self.sync_client[database_name]
        self.sync_collection = self.sync_database[collection_name]

    def build(self):
        for endpoint in EndpointsStatus.ENDPOINTS:
            self.sync_collection.update_one(
                {"endpoint": endpoint},
                {"$set": {"workers": {worker: True for worker in EndpointsStatus.WORKERS}}},
                upsert=True
            )

    async def take_worker(self, endpoint, worker):
        await self.collection.update_one(
            {"endpoint": endpoint},
            {"$set": {f"workers.{worker}": False}}
        )

    async def free_worker(self, endpoint, worker):
        await self.collection.update_one(
            {"endpoint": endpoint},
            {"$set": {f"workers.{worker}": True}}
        )

    async def check_worker(self, endpoint, worker):
        result = await self.collection.find_one(
            {"endpoint": endpoint},
            {f"workers.{worker}": 1, "_id": 0}
        )
        return result['workers'][worker] if result else None

