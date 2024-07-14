from tkinter import Tk, Label, Entry, Button, CENTER, BooleanVar, Checkbutton, IntVar, Radiobutton
import requests
import json
import numpy as np
from scipy.stats import norm
from config import api_key

def main():
    # FRED API key (consider concealing in environmental variable or configuration file)
    #api_key = api_key 
    if not api_key:
        raise ValueError("API Key not found in configuration file")
    create_gui()

def get_treasury_yield(api_key):
    series_id = 'DGS2'
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = json.loads(response.text)
            observations = data["observations"]
            most_recent = observations[-1]
            yield_value = float(most_recent["value"]) / 100
            print("API Call")       # Debug
            return yield_value
        except (KeyError, ValueError) as e:
            print(f"Error parsing data: {e}")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None


def calculate_option_prices(
    option_type_var: IntVar,
    stock_price_entry: Entry,
    strike_price_entry: Entry,
    time_to_expiration_entry: Entry,
    volatility_entry: Entry,
    custom_yield_var: BooleanVar,
    custom_yield_entry: Entry,
    yield_label: Label,
    option_type_label: Label,
    call_price_label: Label,
    put_price_label: Label
    ) -> None:

    """
    Calculates and displays call and put option prices based on user input and selected options.

    Args:
        option_type_var (IntVar): Variable holding the selected option type (0 for Call, 1 for Put)
        stock_price_entry (Entry): Entry widget for user input of stock price
        strike_price_entry (Entry): Entry widget for user input of strike price
        time_to_expiration_entry (Entry): Entry widget for user input of time to expiration (days)
        volatility_entry (Entry): Entry widget for user input of volatility
        custom_yield_var (BooleanVar): Variable indicating if custom yield is used
        custom_yield_entry (Entry): Entry widget for user input of custom yield (if applicable)
        yield_label (Label): Label displaying the risk-free rate value
        option_type_label (Label): Label displaying the selected option type (Call or Put)
        call_price_label (Label): Label displaying the calculated call option price
        put_price_label (Label): Label displaying the calculated put option price

    Returns:
        None
    """
        
    try:
        # Get user input from entry boxes
        option_type = option_type_var.get()  # Get input, remove whitespace, and uppercase
        print("Option type: ", option_type)
        stock_price = float(stock_price_entry.get())
        strike_price = float(strike_price_entry.get())
        time_to_expiration = float(time_to_expiration_entry.get()) / 365  # Convert days to years
        volatility = float(volatility_entry.get())

        # Handle custom risk-free rate based on checkbox state
        if custom_yield_var.get():
            try:
                custom_yield_text = custom_yield_entry.get()
                try:
                    custom_yield = float(custom_yield_text)
                except ValueError:
                    yield_label.config(text="Error: Invalid custom yield. Using default (2.0%).")
                    custom_yield = 0.02
                risk_free_rate = custom_yield/100
                yield_label.config(text=f"{custom_yield:.2}%")  # Update yield label with custom value
                print(f"Using custom risk-free rate: {custom_yield}")
            except ValueError:
                yield_label.config(text="Error: Invalid custom yield. Using default (2.0%).")
                risk_free_rate = 0.02
        else:
            # Retrieve yield from FRED API if checkbox is not selected
            risk_free_rate = get_treasury_yield(api_key)
            if risk_free_rate is None:
                # Handle yield retrieval failure
                yield_label.config(text="Error retrieving yield. Using default (2.0%).")
                risk_free_rate = 0.02
            else:
                yield_label.config(text=f"{risk_free_rate:.2%}")
                print("Risk-free rate: ", risk_free_rate)

        # Validate option type
        if option_type not in (0, 1):
            print("Option type: ", option_type)
            option_type_label.config(text="Error: Invalid option type (Call or Put).")
            call_price_label.config(text="")
            put_price_label.config(text="")
            return

        # Calculate option prices based on valid option type
        if option_type == 0:
            call_price = black_scholes("CALL", stock_price, strike_price, time_to_expiration, risk_free_rate, volatility)
            put_price = None  # Put price not applicable for Call option
            call_price_label.config(text=f"Call Option Price: ${call_price:.2f}" if call_price else "")     # Update labels with calculated prices
            print("Call price: ", call_price)
        elif option_type == 1:
            call_price = None  # Call price not applicable for Put option
            put_price = black_scholes("PUT", stock_price, strike_price, time_to_expiration, risk_free_rate, volatility)
            put_price_label.config(text=f"Put Option Price: ${put_price:.2f}" if put_price else "")         # Update labels with calculated prices
            print("Put price: ", put_price)
        else:
            print("Calculation failed")

    except ValueError:
        # Handle invalid user input (e.g., non-numeric values)
        yield_label.config(text="Error: Invalid input. Please enter numbers.")
        call_price_label.config(text="")
        put_price_label.config(text="")



def black_scholes(call_put, S, K, T, r, sigma):
    """
    Calculates the theoretical price of a European option using the Black-Scholes model.

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

    if call_put == "CALL":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif call_put == "PUT":
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        print("Error: Invalid option type. Please enter 'call' or 'put'.")
        return None

def create_gui():
    window = Tk()
    window.title("Stock Option Pricing")
    window.geometry("500x500")

    option_type_var = IntVar(window)
    option_type_var.set(0)  # Default selection is "call"

    # Option Type Label
    option_type_label = Label(window, text="Option Type:")
    option_type_label.grid(row=0, column=0, padx=5, pady=5)

    # Option Type Buttons
    option_type_button = Radiobutton(window, text="Call", variable=option_type_var, value=0, command=lambda: option_type_var.get())
    option_type_button.grid(row=0, column=1, padx=5, pady=5)

    option_type_button = Radiobutton(window, text="Put", variable=option_type_var, value=1, command=lambda: option_type_var.get())
    option_type_button.grid(row=0, column=2, padx=5, pady=5)

    # Stock Price Label
    stock_price_label = Label(window, text="Stock Price:")
    stock_price_label.grid(row=1, column=0, padx=5, pady=5)

    # Stock Price Entry
    stock_price_entry = Entry(window, width=20)
    stock_price_entry.grid(row=1, column=1, padx=5, pady=5)

    # Strike Price Label
    strike_price_label = Label(window, text="Strike Price:")
    strike_price_label.grid(row=2, column=0, padx=5, pady=5)

    # Strike Price Entry
    strike_price_entry = Entry(window, width=20)
    strike_price_entry.grid(row=2, column=1, padx=5, pady=5)

    # Time to Expiration Label
    time_to_expiration_label = Label(window, text="Time to Expiration (Days):")
    time_to_expiration_label.grid(row=3, column=0, padx=5, pady=5)

    # Time to Expiration Entry
    time_to_expiration_entry = Entry(window, width=20)
    time_to_expiration_entry.grid(row=3, column=1, padx=5, pady=5)

    # Volatility Label
    volatility_label = Label(window, text="Volatility:")
    volatility_label.grid(row=4, column=0, padx=5, pady=5)

    # Volatility Entry
    volatility_entry = Entry(window, width=20)
    volatility_entry.grid(row=4, column=1, padx=5, pady=5)

    # Custom risk-free rate toggle button
    custom_yield_var = BooleanVar(window)  # Boolean variable to track toggle button state
    custom_yield_var_button = Checkbutton(window, text="Use Custom Value for Risk-Free Rate", variable=custom_yield_var, command=lambda: update_custom_yield_entry(custom_yield_var.get(), custom_yield_entry))
    custom_yield_var_button.grid(row=5, columnspan=2, padx=5, pady=5)

    # Custom Risk-Free Rate Label and Entry
    custom_yield_label = Label(window, text="Custom Risk-Free Rate:", state='disabled')
    custom_yield_label.grid(row=6, column=0, padx=5, pady=5)

    custom_yield_entry = Entry(window, width=20, state='disabled')  # Initially disabled
    custom_yield_entry.grid(row=6, column=1, padx=5, pady=5)

    # Risk-Free Rate Label
    yield_label = Label(window, text="Risk-Free Rate:")
    yield_label.grid(row=7, column=0, padx=5, pady=5)

    # Provided by FRED API (initial state)
    yield_label = Label(window, text="Provided by FRED API")
    yield_label.grid(row=7, column=1, padx=5, pady=5)

    # Option Price Labels
    call_price_label = Label(window, text="", anchor=CENTER)  # Set anchor for center alignment
    call_price_label.grid(row=8, column=0, padx=5, pady=5)

    put_price_label = Label(window, text="", anchor=CENTER)  # Set anchor for center alignment
    put_price_label.grid(row=9, column=0, padx=5, pady=5)

    # Calculate Button
    calculate_button = Button(window, text="Calculate", command=lambda: calculate_option_prices(option_type_var, stock_price_entry, strike_price_entry, time_to_expiration_entry, volatility_entry, custom_yield_var, custom_yield_entry, yield_label, option_type_label, call_price_label, put_price_label))
    calculate_button.grid(row=10, columnspan=2, padx=5, pady=5)

    def update_custom_yield_entry(state, entry):
        if state:
            entry.config(state='normal')  # Enable entry if checkbox is selected
        else:
            entry.config(state='disabled')  # Disable entry if checkbox is deselected

    window.mainloop()

if __name__ == "__main__":
    main()