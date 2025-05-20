from fastapi import FastAPI, HTTPException
import uvicorn
from auth_handler import Register, Login
from production_handler import add_production, get_production, update_production, delete_production, get_production_by_farmer
from db_handler import create_base_schema
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from auth_handler import Register, Login, create_access_token
import requests_handler
import farmer_handler

app = FastAPI(
    title="CRM Фермер",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", summary="Root Endpoint", description="Returns a welcome message.")
async def read_root():
    return {"HELLO" : "WORLD"}

@app.post("/api/auth", summary="Authentication Endpoint", description="Handles user authentication.")
async def auth(req: dict):
    try:
        username = req["username"]
        password = req["password"]
        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password are required.")
        if Login(username, password):
            token = create_access_token({"sub": username})
            return JSONResponse(status_code=200, content={"message": "Login successful", "access_token": token})
        else:
            return JSONResponse(status_code=401, content={"message": "Invalid credentials"})
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid request format. Expected JSON with 'username' and 'password' keys.")

@app.post("/api/register", summary="Registration Endpoint", description="Handles user registration.")
async def register(req: dict):
    try:
        username = req["username"]
        password = req["password"]
        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password are required.")
        if Register(username, password):
            return JSONResponse(status_code=200, content={"message": "User registered successfully"})
        else:
            return JSONResponse(status_code=403, content={"message": "User with this username already exists"})
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid request format. Expected JSON with 'username' and 'password' keys.")
    
@app.post("/api/production", summary="Add Production Endpoint", description="Handles adding production.")
async def add_prod(req : dict):
    try:
        name = req["name"]
        quality = req["quality"]
        amount = req["amount"]
        price = req["price"]
        farmer_id = req["farmer_id"]
        if not name or not quality or not amount or not price or not farmer_id:
            raise HTTPException(status_code=400, detail="All fields are required.")
        add_production(name, quality, amount, price, farmer_id)
        return JSONResponse(status_code=201, content={"message": "Production added successfully"})
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid request format. Expected JSON with 'name', 'quality', 'amount', 'price', and 'farmer_id' keys.")
    
@app.get("/api/production", summary="Get Production Endpoint", description="Handles getting all production.")
async def get_prod():
    try:
        production = get_production()
        return JSONResponse(status_code=200, content={"production": production})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/production/{id}", summary="Update Production Endpoint", description="Handles updating production.")
async def update_prod(id: int, req : dict):
    try:
        name = req["name"]
        quality = req["quality"]
        amount = req["amount"]
        price = req["price"]
        if not name or not quality or not amount or not price:
            raise HTTPException(status_code=400, detail="All fields are required.")
        update_production(id, name, quality, amount, price)
        return JSONResponse(status_code=200, content={"message": "Production updated successfully"})
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid request format. Expected JSON with 'name', 'quality', 'amount', and 'price' keys.")

@app.delete("/api/production/{id}", summary="Delete Production Endpoint", description="Handles deleting production.")
async def delete_prod(id):
    try:
        delete_production(id)
        return JSONResponse(status_code=200, content={"message": "Production deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/production/farmer/{farmer_id}", summary="Get Production by Farmer Endpoint", description="Handles getting production by farmer ID.")
async def get_prod_by_farmer(farmer_id: int):
    try:
        production = get_production_by_farmer(farmer_id)
        return JSONResponse(status_code=200, content={"production": production})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/requests", summary="Add Request Endpoint", description="Handles adding requests.")
async def add_req(req : dict):
    try:
        name = req["name"]
        good = req["good"]
        category = req["category"]
        cost = req["cost"]
        farmer_id = req["farmer_id"]
        if not name or not good or not category or not cost or not farmer_id:
            raise HTTPException(status_code=400, detail="All fields are required.")
        requests_handler.add_request(name, good, category, cost, farmer_id)
        return JSONResponse(status_code=201, content={"message": "Request added successfully"})
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid request format. Expected JSON with 'name', 'good', 'category', 'cost', and 'farmer_id' keys.")
    
@app.get("/api/requests", summary="Get Requests Endpoint", description="Handles getting all requests.")
async def get_req():
    try:
        requests = requests_handler.get_requests()
        return JSONResponse(status_code=200, content={"requests": requests})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/api/requests/{id}", summary="Update Request Endpoint", description="Handles updating requests.")
async def update_req(id: int, req : dict):
    try:
        name = req["name"]
        good = req["good"]
        category = req["category"]
        cost = req["cost"]
        if not name or not good or not category or not cost:
            raise HTTPException(status_code=400, detail="All fields are required.")
        requests_handler.update_request(id, name, good, category, cost)
        return JSONResponse(status_code=200, content={"message": "Request updated successfully"})
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid request format. Expected JSON with 'name', 'good', 'category', and 'cost' keys.")
    
@app.delete("/api/requests/{id}", summary="Delete Request Endpoint", description="Handles deleting requests.")
async def delete_req(id: int):
    try:
        requests_handler.delete_request(id)
        return JSONResponse(status_code=200, content={"message": "Request deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/requests/farmer/{farmer_id}", summary="Get Requests by Farmer Endpoint", description="Handles getting requests by farmer ID.")
async def get_req_by_farmer(farmer_id: int):
    try:
        requests = requests_handler.get_requests_by_farmer(farmer_id)
        return JSONResponse(status_code=200, content={"requests": requests})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/farmers", summary="Get Farmers Endpoint", description="Handles getting all farmers.")
async def get_farmers():
    try:
        farmers = farmer_handler.get_farmers()
        return JSONResponse(status_code=200, content={"farmers": farmers})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/farmers", summary="Add Farmer Endpoint", description="Handles adding farmers.")
async def add_farmer(req : dict):
    try:
        name = req["name"]
        surname = req["surname"]
        patr = req["patr"]
        if not name or not surname or not patr:
            raise HTTPException(status_code=400, detail="All fields are required.")
        farmer_handler.add_farmer(name, surname, patr)
        return JSONResponse(status_code=201, content={"message": "Farmer added successfully"})
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid request format. Expected JSON with 'name', 'surname', and 'patr' keys.")

@app.put("/api/farmers/{id}", summary="Update Farmer Endpoint", description="Handles updating farmers.")
async def update_farmer(id: int, req : dict):
    try:
        name = req["name"]
        surname = req["surname"]
        patr = req["patr"]
        if not name or not surname or not patr:
            raise HTTPException(status_code=400, detail="All fields are required.")
        farmer_handler.update_farmer(id, name, surname, patr)
        return JSONResponse(status_code=200, content={"message": "Farmer updated successfully"})
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid request format. Expected JSON with 'name', 'surname', and 'patr' keys.")

@app.delete("/api/farmers/{id}", summary="Delete Farmer Endpoint", description="Handles deleting farmers.")
async def delete_farmer(id: int):
    try:
        farmer_handler.delete_farmer(id)
        return JSONResponse(status_code=200, content={"message": "Farmer deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/farmers/{id}", summary="Get Farmer by ID Endpoint", description="Handles getting a farmer by ID.")
async def get_farmer_by_id(id: int):
    try:
        farmer = farmer_handler.get_farmer_by_id(id)
        if not farmer:
            raise HTTPException(status_code=404, detail="Farmer not found.")
        return JSONResponse(status_code=200, content={"farmer": farmer})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)