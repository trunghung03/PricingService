from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import random
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the CSV file
file_path = 'diamonds.csv'
diamonds_df = pd.read_csv(file_path)
metal_file_path = 'metals.csv'
metals_df = pd.read_csv(metal_file_path)

class DiamondRequest(BaseModel):
    cut: str
    carat: float
    clarity: str
    color: str
    
# Model for metal price request
class MetalRequest(BaseModel):
    name: str

def read_fluctuation(file_path: str) -> float:
    """
    Reads the fluctuation percentage from a file.

    Parameters:
    file_path (str): The path to the fluctuation file

    Returns:
    float: The fluctuation percentage
    """
    try:
        with open(file_path, 'r') as file:
            fluctuation = float(file.read().strip())
        return fluctuation
    except Exception as e:
        raise RuntimeError(f"Error reading fluctuation file: {e}")

def write_fluctuation(file_path: str, value: float):
    """
    Writes a new fluctuation percentage to a file.

    Parameters:
    file_path (str): The path to the fluctuation file
    value (float): The new fluctuation percentage
    """
    try:
        with open(file_path, 'w') as file:
            file.write(str(value))
    except Exception as e:
        raise RuntimeError(f"Error writing to fluctuation file: {e}")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/diamond_price/")
def get_diamond_price(diamond: DiamondRequest):
    """
    Endpoint to get the price of a diamond based on its cut, carat, clarity, and color.
    Adjusts the price based on a fluctuation percentage from an external file.
    
    Parameters:
    diamond (DiamondRequest): The 4C values of the diamond
    
    Returns:
    dict: The adjusted price of the diamond if found, otherwise an error message
    """
    # File path for the fluctuation percentage
    fluctuation_file_path = 'fluctuation.txt'

    # Read the fluctuation percentage
    fluctuation = read_fluctuation(fluctuation_file_path)

    # Filter the DataFrame based on the given criteria
    filtered_df = diamonds_df[
        (diamonds_df['cut'] == diamond.cut) &
        (diamonds_df['carat'] == diamond.carat) &
        (diamonds_df['clarity'] == diamond.clarity) &
        (diamonds_df['color'] == diamond.color)
    ]
    
    # If a matching diamond is found, adjust its price, otherwise raise an HTTPException
    if not filtered_df.empty:
        base_price = int(filtered_df.iloc[0]['price'])  # Convert numpy.int64 to int
        adjusted_price = base_price * (1 + fluctuation / 100)  # Apply fluctuation
        return {"price": adjusted_price}
    else:
        raise HTTPException(status_code=404, detail="Diamond not found")

# Endpoint to get the price of a rare metal
@app.post("/metal_price/")
def get_metal_price(metal: MetalRequest):
    """
    Endpoint to get the price of a metal based on its name.
    Adjusts the price based on a fluctuation percentage from an external file.
    
    Parameters:
    metal (MetalRequest): The name of the metal
    
    Returns:
    dict: The adjusted price of the metal if found, otherwise an error message
    """
    fluctuation_file_path = 'fluctuation.txt'
    metal_prices_file_path = 'metals_pricing.csv'
    
    fluctuation = read_fluctuation(fluctuation_file_path)
    
    filtered_df = metals_df[metals_df['name'] == metal.name]
    
    if not filtered_df.empty:
        base_price = int(filtered_df.iloc[0]['price'])
        adjusted_price = base_price * (1 + fluctuation / 100)
        return {"price": adjusted_price}
    else:
        raise HTTPException(status_code=404, detail="Metal not found")

@app.post("/update_fluctuation/")
def update_fluctuation():
    """
    Endpoint to update the fluctuation percentage to a random number between 1 and 5.
    
    Returns:
    dict: The new fluctuation percentage
    """
    fluctuation_file_path = 'fluctuation.txt'
    new_fluctuation = random.uniform(1, 5)
    write_fluctuation(fluctuation_file_path, new_fluctuation)
    return {"new_fluctuation": new_fluctuation}

# Example usage
cut = 'Ideal'
carat = 0.23
clarity = 'SI2'
color = 'E'
price = get_diamond_price(DiamondRequest(cut=cut, carat=carat, clarity=clarity, color=color))
print(f"The price of the diamond is: {price}")
