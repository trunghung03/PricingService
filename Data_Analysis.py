import pandas as pd

def get_column_value():
    # Extract distinct values for each column
    distinct_values = {column: diamonds_df[column].unique().tolist() for column in diamonds_df.columns}

    # Print the distinct values for each column
    for column, values in distinct_values.items():
        print(f"Column: {column}")
        print(f"Distinct values ({len(values)}): {values}\n")
        
def get_diamond_price(cut, carat, clarity, color):
    """
    Function to get the price of a diamond based on its cut, carat, clarity, and color.
    
    Parameters:
    cut (str): The cut of the diamond (e.g., 'Ideal', 'Premium', 'Good', 'Very Good', 'Fair')
    carat (float): The carat weight of the diamond
    clarity (str): The clarity of the diamond (e.g., 'SI1', 'VS1', 'VS2', etc.)
    color (str): The color of the diamond (e.g., 'E', 'I', 'J', etc.)
    
    Returns:
    int: The price of the diamond if found, otherwise None
    """
    # Filter the DataFrame based on the given criteria
    filtered_df = diamonds_df[
        (diamonds_df['cut'] == cut) &
        (diamonds_df['carat'] == carat) &
        (diamonds_df['clarity'] == clarity) &
        (diamonds_df['color'] == color)
    ]
    
    # If a matching diamond is found, return its price, otherwise return None
    if not filtered_df.empty:
        return filtered_df.iloc[0]['price']
    else:
        return None


file_path = 'diamonds.csv'
diamonds_df = pd.read_csv(file_path)

# get_column_value()
cut = 'Ideal'
carat = 0.23
clarity = 'SI2'
color = 'E'
price = get_diamond_price(cut, carat, clarity, color)
print(f"The price of the diamond is: {price}")
