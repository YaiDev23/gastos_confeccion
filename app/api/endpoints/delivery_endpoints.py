from fastapi import APIRouter

router = APIRouter()

class DeliveryEndpoints:
    @router.get("/deliveries")
    async def get_deliveries(self):
        return {"message": "List of deliveries"}

    @router.post("/deliveries")
    async def create_delivery(self):
        return {"message": "Delivery created"}