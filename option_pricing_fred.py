from tkinter import Tk, Label, Entry, Button   # For GUI
import requests                 # For API request
import json                     # For parse API response
import numpy as np              # For Black-Scholes Model calculations
from scipy.stats import norm    # For Black-Scholes Model (z-score of cumulative distribution function (CDF) of the standard normal distribution)

# Your FRED API key
api_key = 'd04e0528daa3aa373b4bf283a573211c' 
def main():
    print("Theoretical option price:", calculate_option_price())


def black_scholes(call_put, S, K, T, r, sigma):
  """
  This function calculates the theoretical price of a European option (can only be exercised at expiration) using the Black-Scholes model.

  Args:
      call_put (str): "call" for call option, "put" for put option
      S (float): Current stock price
      K (float): Strike price
      T (float): Time to expiration in years (e.g., 0.5 for 6 months)
      r (float): Risk-free interest rate (e.g., 0.05 for 5%)
      sigma (float): Volatility of the underlying stock (annualized)

  Returns:
      float: Theoretical price of the option
  """
  d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
  d2 = d1 - sigma * np.sqrt(T)

  if call_put == "call":
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
  elif call_put == "put":
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
  else:
    print("Error: Invalid option type. Please enter 'call' or 'put'.")
    return None

# Function to get the 2-year treasury yield from FRED API
def get_treasury_yield():
    api_key = 'd04e0528daa3aa373b4bf283a573211c'
    series_id = 'DGS2'
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json"
    response = requests.get(url)

    # Check for successful response
    if response.status_code == 200:
        try:
            # Parse the JSON data
            data = json.loads(response.text)
            observations = data["observations"]
            most_recent = observations[-1]
            yield_value = float(most_recent["value"])/100
            return yield_value
        except (KeyError, ValueError) as e:
            print(f"Error parsing data: {e}")
            return None  # Indicate failure by returning None
    else:
        print(f"Error: {response.status_code}")
        return None

def calculate_option_price():
    option_type = input("Option type: ")                            #call
    stock_price = float(input("Stock price: "))                     #11.82
    strike_price = float(input("Strike price: "))                   #11.50
    time_to_expiration = float(input("Days to expiration: "))/365   #18
    # Get the 2-year treasury yield from FRED API
    risk_free_rate = get_treasury_yield()
    volatility = 0.3  # annualized

    # Handle the case where yield retrieval fails
    if risk_free_rate is None:
        print("Failed to retrieve yield data. Using default value (2.0%).")
        risk_free_rate = 0.02
        
    while True:
        option_type = option_type.strip().upper()  # Get input, remove whitespace, and uppercase
        if option_type in ("CALL", "PUT"):
            break  # Valid option type, exit loop
        else:
            option_type.delete(0, 'end')  # Clear the entry box
            option_type.config(text="Error: Invalid option type (Call or Put).")

    # Calculate option prices based on valid option type
    if option_type == "CALL":
        call_price = black_scholes("call", stock_price, strike_price, time_to_expiration, risk_free_rate, volatility)
        put_price = None  # Put price not applicable for Call option
        return call_price
    elif option_type == "PUT":
        call_price = None  # Call price not applicable for Put option
        put_price = black_scholes("put", stock_price, strike_price, time_to_expiration, risk_free_rate, volatility)
        return put_price
    

if __name__ == "__main__":
    main()