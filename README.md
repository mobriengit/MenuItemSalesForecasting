# Menu Item Sales Forecasting and Inventory Analysis

This repository contains a Python script for forecasting sales of menu items in the restaurant industry and analyzing inventory needs. The model uses historical sales data to predict future demand and provides insights into whether products have been over-ordered or under-ordered based on the forecasted demand.

Data Loading and Preparation

The script loads the menu_items.csv file and prepares the data by simulating daily demand values for each product.
Daily demand is calculated by evenly distributing the monthly demand across 30 days.
Forecasting

Uses the Prophet library to forecast future demand for each product based on the prepared daily demand data.
Generates a 30-day forecast for each product.
Inventory Analysis

Compares the predicted demand with the baseline order to determine if products were over-ordered or under-ordered.
Saves the analysis results to purchase_requirements.csv.
Visualization

Sales Forecast Plot: Plots the predicted demand for a sample product.
Double-Sided Bar Graph: Visualizes the difference between predicted demand and baseline orders, highlighting over-ordered and under-ordered products.

Example Output
Sales Forecast Plot for a Sample Product:

Double-Sided Bar Graph for Over-Ordered and Under-Ordered Products:

Key Functions
prepare_data(df, product_id): Prepares the data for the Prophet model by simulating daily demand.
forecast_demand(df, product_id, periods=30): Generates a 30-day forecast using the Prophet model.
main(): Main function that runs the forecasting and analysis, and generates visualizations.
Output Files
purchase_requirements.csv: Contains the analysis results showing which products need to be purchased based on the forecasted demand.
Contributing
Feel free to submit pull requests or report issues. Contributions are welcome!

