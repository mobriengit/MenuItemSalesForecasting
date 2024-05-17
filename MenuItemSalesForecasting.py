import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('/Users/mattobrien/Downloads/Menu_Items_Data.csv')

# Debug: Print the first few rows and columns of the DataFrame to ensure it is loaded correctly
print("Data Loaded:")
print(data.head())

# Convert ProductID to string for better visualization
data['ProductID'] = data['ProductID'].astype(str)

# Prepare the data for Prophet
def prepare_data(df, product_id):
    product_data = df[df['ProductID'] == product_id][['PastMonthDemand']]
    total_days = 30  # Assuming a month has 30 days
    
    # Simulate daily demand by distributing the monthly demand evenly across the days
    daily_demand = product_data['PastMonthDemand'].values[0] / total_days
    dates = pd.date_range(start='2023-01-01', periods=total_days, freq='D')
    
    df_prepared = pd.DataFrame({
        'ds': dates,
        'y': [daily_demand] * total_days
    })
    
    # Debug: Check if the prepared data is correct
    print(f"Prepared data for ProductID: {product_id}")
    print(df_prepared.head())
    
    return df_prepared

# Forecasting function
def forecast_demand(df, product_id, periods=30):
    df_prepared = prepare_data(df, product_id)
    model = Prophet()
    model.fit(df_prepared)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return model, forecast

# Two-tiered analysis: forecasting and required products for purchase
product_forecasts = {}
purchase_requirements = []

for product_id in data['ProductID'].unique():
    model, forecast = forecast_demand(data, product_id)
    product_name = data[data['ProductID'] == product_id]['ProductName'].values[0]
    product_forecasts[product_name] = forecast
    
    # Determine required products for purchase
    last_demand = data[data['ProductID'] == product_id]['PastMonthDemand'].values[-1]
    predicted_demand = forecast['yhat'].values[-1] * 30  # Scale back to monthly demand
    baseline_order = data[data['ProductID'] == product_id]['BaselineOrder'].values[0]
    
    if predicted_demand > last_demand:
        purchase_amount = predicted_demand - last_demand
        purchase_requirements.append({
            'ProductID': product_id,
            'ProductName': product_name,
            'PredictedDemand': predicted_demand,
            'LastDemand': last_demand,
            'BaselineOrder': baseline_order,
            'PurchaseAmount': purchase_amount
        })

# Convert purchase requirements to DataFrame
purchase_df = pd.DataFrame(purchase_requirements)

# Handle the case where no products need to be purchased
if not purchase_df.empty:
    purchase_df = purchase_df.sort_values(by='PurchaseAmount', ascending=False)
    # Save purchase requirements to CSV
    purchase_df.to_csv('purchase_requirements.csv', index=False)
    print("Purchase requirements saved to 'purchase_requirements.csv'.")
else:
    print("No products require additional purchases based on the forecast.")

# Plotting the forecast for a sample product
if product_forecasts:
    sample_product = list(product_forecasts.keys())[0]
    forecast = product_forecasts[sample_product]

    plt.figure(figsize=(10, 6))
    plt.plot(forecast['ds'], forecast['yhat'], label='Predicted Demand')
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.2)
    plt.title(f'Sales Forecast for {sample_product}')
    plt.xlabel('Date')
    plt.ylabel('Demand')
    plt.legend()
    plt.show()

# Double-Sided Bar Graph for Over-Ordered and Under-Ordered Products
if not purchase_df.empty:
    purchase_df['Difference'] = purchase_df['PredictedDemand'] - purchase_df['BaselineOrder']
    
    over_ordered = purchase_df[purchase_df['Difference'] < 0]
    under_ordered = purchase_df[purchase_df['Difference'] > 0]

    plt.figure(figsize=(14, 7))
    plt.barh(over_ordered['ProductName'], over_ordered['Difference'], color='red', label='Over-Ordered')
    plt.barh(under_ordered['ProductName'], under_ordered['Difference'], color='green', label='Under-Ordered')
    plt.axvline(0, color='black', linewidth=0.8)
    plt.xlabel('Difference (Predicted Demand - Baseline Order)')
    plt.ylabel('Product Name')
    plt.title('Over-Ordered and Under-Ordered Products')
    plt.legend()
    plt.show()

print("Forecasting and analysis complete.")

