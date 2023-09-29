from fastapi import FastAPI
from src.controller.routes import (person_routes,
                                   product_routes,
                                    warehouse_routes,
                                    product_count_routes,
                                    inventory_routes
                                )
from src.controller.auth import authentication

app = FastAPI()
app.include_router(authentication.router)
app.include_router(person_routes.router)
app.include_router(product_routes.router)
app.include_router(warehouse_routes.router)
app.include_router(product_count_routes.router)
app.include_router(inventory_routes.router)

@app.get("/", tags=['home'])
async def root():
    return {"message": "Inventory Project"}
