from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY")) 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)

class Item(BaseModel):
    id: int
    items: Dict[str, int]

class OrderItem(BaseModel):
    burgers: int
    fries: int
    drinks: int

class OrderRequest(BaseModel):
    text: str

class Order(BaseModel):
    id: int
    items: OrderItem

orders = [
    # Item(id=1, items={"burgers": 3, "fries": 2, "drinks": 5}),
    # Item(id=2, items={"burgers": 1, "fries": 1, "drinks": 2}),
]

if orders:
    last_id = max(order.id for order in orders)
else:
    last_id = 0

def send_message_to_LLM(order_text: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Extract structured orders or commands like 'order 3 fries' or 'delete order 2'. If it is an order, format: burgers: int, fries: int, drinks: int. If it is a delete, format: delete: int"},
            {"role": "user", "content": order_text},
        ],
        temperature=0
    )

    return response.choices[0].message.content

def parse_order(llm_order: str):
    global last_id
    llm_order.replace('order', '')
    order_text = llm_order.strip('{}')
    items = order_text.split(',')
    order_dict = {}

    for item in items:
        key, value = item.split(':')
        key = key.strip()
        value = int(value.strip())
        order_dict[key] = value

    last_id += 1
    new_order = Item(id=last_id, items=order_dict)

    return new_order

def parse_delete(llm_order: str):
    delete_id = llm_order.split(":")[1]
    return int(delete_id)

@app.get("/api/items", response_model=List[Item])
async def get_items():
    return orders

@app.post("/api/order")
async def create_order_or_delete(order_request: OrderRequest):
    llm_response = send_message_to_LLM(order_request.text)

    if "delete" in llm_response:
        delete_id = parse_delete(llm_response)
        deleted_order = await delete_order(delete_id)
        return {"message": "Order deleted", "order": deleted_order}
    else:
        new_order = parse_order(llm_response)
        orders.append(new_order)
        return {"message": "Order received", "order": new_order}

@app.delete("/api/order/{order_id}")
async def delete_order(order_id: int):
    global orders
    order_to_delete = {}

    for order in orders:
        if order.id == order_id:
            order_to_delete = order
            break
    
    orders = [order for order in orders if order.id != order_id]
    
    return order_to_delete