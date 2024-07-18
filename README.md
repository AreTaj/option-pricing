# Option Pricing
#### Video Demo:  <https://youtu.be/>
#### Description: 
Aresh Tajvar, 2024
CS50x Final Project
Option Pricing

Github repository:
https://github.com/AreTaj/option-pricing

Harvard CS50 Python Final Project:
https://cs50.harvard.edu/x/2024/project/

St. Louis Federal Reserve Economic Data API Documentation:
https://fred.stlouisfed.org/docs/api/fred/

This program is designed to calculate the price of a financial derivative call or put option using the Black-Scholes option pricing model. The input values for the model come from  user input fields in the graphical user interface (GUI) and, for the risk-free rate, from the most recently published 2-year bond available from the FRED API; 2-year bond yield is commonly used as a risk-free rate in financial modeling.

Introduction:
This program is a CS50x Final Project created by Aresh Tajvar in 2024. It calculates theoretical prices for call and put options using the Black-Scholes model an is iteracted with through a graphical user interface (GUI).

Functionality Overview:
The program offers a user-friendly GUI built with Tkinter, allowing users to input key option details:
•	Option Type (Call or Put)
•	Stock Price
•	Strike Price
•	Time to Expiration (in Days)
•	Volatility

Risk-Free Rate Integration:
•	To incorporate the risk-free rate, a key component in option pricing and most financial models, the program utilizes the St. Louis Federal Reserve's Economic Data (FRED) API.
•	By default, it retrieves the most recent yield data for the 2-year Treasury bond, which is a very common proxy for the risk-free rate in financial modeling.

Optional Custom Risk-Free Rate:
•	The program acknowledges that the user may want to use a different risk-free rate than the common 2-year bond yield, which might not always be the ideal risk-free rate for all scenarios.
•	It offers a functionality where users can choose to input a custom risk-free rate value.

Theoretical Option Price Calculation:
•	Once all inputs are gathered, the program employs the Black-Scholes formula to calculate the theoretical price for the chosen option type (call or put).
•	The calculated prices are displayed on the GUI for both call and put options.

Underlying Components:
•	Libraries: The program relies on several Python libraries for its functionality:
        o	tkinter for building the user interface.
        o	requests and json for interacting with the FRED API.
        o	numpy for numerical computations.
        o	scipy.stats.norm for accessing the normal cumulative distribution function (CDF), a necessary element in the Black-Scholes formula.
•	Core Functions:
        o	get_treasury_yield: This function handles retrieving the 2-year treasury yield from the FRED API and gracefully handles potential errors like API unavailability or invalid data format.
        o	calculate_option_prices: This core function processes user input, retrieves the risk-free rate, validates input types, and calculates option prices using the black_scholes function. It's also responsible for updating the GUI labels with the calculated prices or informative error messages.
        o	black_scholes: This function implements the Black-Scholes formula, the brains behind the option pricing calculations. It takes the provided parameters and calculates the theoretical price for a call or put European option, meaning the option is held to expiration.

Current Limitations and Future Enhancements:
    o	Strengthening error handling mechanisms to catch invalid user input beyond value types (e.g., negative stock prices).
    o	Enriching the user experience by incorporating a graph that visually represents how option prices fluctuate with changes in input values.
    
Using the Program:
1.	Save the code as a Python file (e.g., option_pricing.py).
2.	Ensure you have the required libraries (tkinter, requests, json, numpy, and scipy) installed. You can install them using pip install tkinter requests json numpy scipy.
3.	Securely store your FRED API key in the api_key variable.
4.	Execute the program from the command line using: python option_pricing.py.
5.	Interact with the GUI elements by entering option details and clicking the "Calculate" button to trigger the calculations.

Disclaimer:
The Black-Scholes model serves as a theoretical framework and might not perfectly reflect real-world option prices due to various market factors. This program is designed for educational purposes only and should not be used for making financial investment decisions.
