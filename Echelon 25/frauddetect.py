import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, State
import numpy as np
import json
from datetime import datetime

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Sample data from the provided information
data = [
    {"Customer_ID":"ae480c1c-9745-4d76-93ac-346ef28ddb26","Customer_Location":"Christopherland","Product_ID":"d5e29dd8-9f1d-4f50-86c4-75a01c459f76","Product_Category":"Sweaters","Order_ID":"992df5e1-c6f2-4e0d-b871-ec48402d8b81","Order_Date":"19-02-2025","Order_Amount":64.9,"Payment_Method":"PayPal","Discount_Applied":7.19,"Order_Status":"Returned","Orders_Replaced":1,"Return_Reason":"Size Issue","Device_Used":"Mobile","Browsing_Time":18.43,"Fraudulent_Activity":8},
    {"Customer_ID":"ed203761-7216-450c-a188-ab5a912fb354","Customer_Location":"Jordanton","Product_ID":"fc7c034d-272e-4877-a1e1-90b798608a96","Product_Category":"Shoes","Order_ID":"1fff79d3-ad16-420e-b2c2-ff3c862c5d9b","Order_Date":"06-03-2025","Order_Amount":138.29,"Payment_Method":"Gift Card","Discount_Applied":23.3,"Order_Status":"Returned","Orders_Replaced":1,"Return_Reason":"Defect","Device_Used":"Mobile","Browsing_Time":13.68,"Fraudulent_Activity":8},
    {"Customer_ID":"039f040e-a848-4c4e-b83c-9b18e40a9fc7","Customer_Location":"Laurenfurt","Product_ID":"c9c3e5d5-854e-4917-96e0-c7c9f9dc1d0b","Product_Category":"Shoes","Order_ID":"dde25f35-aadf-4643-bd83-607300a79294","Order_Date":"28-01-2025","Order_Amount":62.21,"Payment_Method":"Debit Card","Discount_Applied":11.99,"Order_Status":"Pending","Orders_Replaced":0,"Return_Reason":"N/A","Device_Used":"Tablet","Browsing_Time":28.52,"Fraudulent_Activity":6},
    {"Customer_ID":"a756821b-17a4-4fdf-a4c0-73aea88b3432","Customer_Location":"South Catherine","Product_ID":"238c92da-48d3-4edf-b38f-e0ed9ce1aab9","Product_Category":"T-Shirts","Order_ID":"124b2170-1365-4b43-9baa-236081055458","Order_Date":"05-03-2025","Order_Amount":345.45,"Payment_Method":"COD","Discount_Applied":18.82,"Order_Status":"Completed","Orders_Replaced":0,"Return_Reason":"N/A","Device_Used":"Tablet","Browsing_Time":27.18,"Fraudulent_Activity":8},
    {"Customer_ID":"deb0ea59-779b-45de-8e37-d4cc3d5b8410","Customer_Location":"Melindaberg","Product_ID":"6ffee7d4-b94b-4e97-a6f9-2b51774d71cc","Product_Category":"T-Shirts","Order_ID":"d306389f-f04e-423a-8218-315854804ed9","Order_Date":"04-02-2025","Order_Amount":179,"Payment_Method":"Credit Card","Discount_Applied":8.97,"Order_Status":"Completed","Orders_Replaced":0,"Return_Reason":"N/A","Device_Used":"Desktop","Browsing_Time":17.65,"Fraudulent_Activity":3},
    {"Customer_ID":"ebae3c55-bf65-46f0-8183-f63f6faf860a","Customer_Location":"Wagnerport","Product_ID":"1687d42f-6ea5-400d-a126-a18ba543ee83","Product_Category":"T-Shirts","Order_ID":"e66b0663-44b1-4540-8940-268d7ec1fd17","Order_Date":"30-01-2025","Order_Amount":424.2,"Payment_Method":"Debit Card","Discount_Applied":17.17,"Order_Status":"Cancelled","Orders_Replaced":0,"Return_Reason":"N/A","Device_Used":"Tablet","Browsing_Time":4.12,"Fraudulent_Activity":4},
    {"Customer_ID":"f25a88f4-a307-4247-920f-eaac9b7562d3","Customer_Location":"Melissafort","Product_ID":"22db8ff9-5cba-491e-b4a5-e308ef14d37f","Product_Category":"Dresses","Order_ID":"82884b21-5f08-4621-9bba-ed83c7cc3c1c","Order_Date":"15-02-2025","Order_Amount":49.88,"Payment_Method":"Gift Card","Discount_Applied":1.93,"Order_Status":"Returned","Orders_Replaced":0,"Return_Reason":"Late Delivery","Device_Used":"Tablet","Browsing_Time":11.09,"Fraudulent_Activity":2},
    {"Customer_ID":"ed6752bd-6d76-4ce8-9cb4-ac613a0d24b2","Customer_Location":"Frostmouth","Product_ID":"9fed6665-881a-45f7-af7c-edf2157434a5","Product_Category":"Dresses","Order_ID":"383bddcf-28d1-4af9-bdac-353cb3fba7a3","Order_Date":"02-01-2025","Order_Amount":65.11,"Payment_Method":"COD","Discount_Applied":27.42,"Order_Status":"Cancelled","Orders_Replaced":0,"Return_Reason":"N/A","Device_Used":"Desktop","Browsing_Time":28.76,"Fraudulent_Activity":10},
    {"Customer_ID":"77f789b4-8d00-4f66-8999-674075072ce1","Customer_Location":"North Codymouth","Product_ID":"b767abda-7e93-4a9c-970c-34a9baea4482","Product_Category":"Shoes","Order_ID":"c810f1a7-769d-4d35-bfeb-67ae8f97ec3d","Order_Date":"11-01-2025","Order_Amount":228.86,"Payment_Method":"COD","Discount_Applied":27.58,"Order_Status":"Returned","Orders_Replaced":0,"Return_Reason":"Defect","Device_Used":"Tablet","Browsing_Time":19.15,"Fraudulent_Activity":3},
    {"Customer_ID":"6ca6e84e-3212-4fa3-aa5c-097546a5057a","Customer_Location":"Phillipside","Product_ID":"da87c035-c5d7-49c5-80b1-bb9980d23c00","Product_Category":"Jeans","Order_ID":"6dd2d1e4-8715-4a57-a21c-4c7296f00cbc","Order_Date":"10-01-2025","Order_Amount":367.5,"Payment_Method":"PayPal","Discount_Applied":1.72,"Order_Status":"Pending","Orders_Replaced":0,"Return_Reason":"N/A","Device_Used":"Tablet","Browsing_Time":20.1,"Fraudulent_Activity":7}
]

# Convert to DataFrame
df = pd.DataFrame(data)

# Convert Order_Date to datetime format
df['Order_Date'] = pd.to_datetime(df['Order_Date'], format="%d-%m-%Y")

# Create date columns for filtering
df['Month'] = df['Order_Date'].dt.month_name()
df['Year'] = df['Order_Date'].dt.year
df['IsRecent'] = (datetime.now() - df['Order_Date']).dt.days <= 30

# Define functions for data processing
def calculate_fraud_risk_levels(filtered_df, threshold=7):
    """Calculate the number of orders in each fraud risk category"""
    high = len(filtered_df[filtered_df['Fraudulent_Activity'] >= 8])
    medium = len(filtered_df[(filtered_df['Fraudulent_Activity'] >= 5) & (filtered_df['Fraudulent_Activity'] < 8)])
    low = len(filtered_df[filtered_df['Fraudulent_Activity'] < 5])
    return {'low': low, 'medium': medium, 'high': high}

def get_payment_method_distribution(filtered_df):
    """Get the distribution of payment methods"""
    return filtered_df['Payment_Method'].value_counts().to_dict()

def get_anomaly_data(filtered_df, threshold=7):
    """Get data points with fraud score above threshold"""
    anomalies = filtered_df[filtered_df['Fraudulent_Activity'] >= threshold].copy()
    if not anomalies.empty:
        anomalies['id_short'] = anomalies['Order_ID'].str[:8]
    return anomalies

def get_sentiment_data(filtered_df):
    """Calculate sentiment based on return reasons"""
    return_reasons = filtered_df[filtered_df['Return_Reason'] != 'N/A']['Return_Reason']
    
    # Initialize counters
    positive = 0
    neutral = 0
    negative = 0
    
    for reason in return_reasons:
        if reason == 'Size Issue':
            neutral += 1
        elif reason in ['Defect', 'Late Delivery']:
            negative += 1
        else:
            positive += 1
    
    return {'positive': positive, 'neutral': neutral, 'negative': negative}

def get_fraud_by_category(filtered_df):
    """Calculate average fraud score by product category"""
    return filtered_df.groupby('Product_Category')['Fraudulent_Activity'].mean().reset_index()

# App layout
app.layout = html.Div(
    style={'backgroundColor': '#f5f5f5', 'minHeight': '100vh', 'padding': '20px'},
    children=[
        html.Div(
            className='container',
            style={'maxWidth': '1200px', 'margin': '0 auto'},
            children=[
                html.H1("Fraud Detection & Sentiment Analysis Dashboard", 
                       style={'fontSize': '28px', 'fontWeight': 'bold', 'marginBottom': '20px', 'color': '#2C3E50'}),
                
                # Filters
                html.Div(
                    style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.12)', 'marginBottom': '20px'},
                    children=[
                        html.Div(
                            style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1fr', 'gap': '20px'},
                            children=[
                                html.Div([
                                    html.Label("Product Category", style={'fontWeight': 'medium', 'marginBottom': '5px', 'display': 'block'}),
                                    dcc.Dropdown(
                                        id='category-filter',
                                        options=[{'label': 'All Categories', 'value': 'All'}] + 
                                                [{'label': cat, 'value': cat} for cat in df['Product_Category'].unique()],
                                        value='All',
                                        style={'width': '100%'}
                                    )
                                ]),
                                html.Div([
                                    html.Label("Fraud Threshold", style={'fontWeight': 'medium', 'marginBottom': '5px', 'display': 'block'}),
                                    dcc.Slider(
                                        id='fraud-threshold',
                                        min=1,
                                        max=10,
                                        value=7,
                                        marks={i: str(i) for i in range(1, 11)},
                                        step=1
                                    ),
                                    html.Div(id='threshold-value', style={'fontSize': '12px', 'color': '#6c757d', 'marginTop': '5px'})
                                ]),
                                html.Div([
                                    html.Label("Date Range", style={'fontWeight': 'medium', 'marginBottom': '5px', 'display': 'block'}),
                                    dcc.Dropdown(
                                        id='date-range-filter',
                                        options=[
                                            {'label': 'All Time', 'value': 'all'},
                                            {'label': 'Last 30 Days', 'value': 'recent'},
                                            {'label': 'January', 'value': 'Jan'},
                                            {'label': 'February', 'value': 'Feb'},
                                            {'label': 'March', 'value': 'Mar'}
                                        ],
                                        value='all',
                                        style={'width': '100%'}
                                    )
                                ])
                            ]
                        )
                    ]
                ),
                
                # Summary Cards
                html.Div(
                    style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1fr 1fr', 'gap': '20px', 'marginBottom': '20px'},
                    children=[
                        html.Div(
                            style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.12)'},
                            children=[
                                html.H3("Total Orders", style={'fontSize': '18px', 'fontWeight': 'semibold', 'marginBottom': '10px', 'color': '#6c757d'}),
                                html.P(id='total-orders', style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#3498db'})
                            ]
                        ),
                        html.Div(
                            style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.12)'},
                            children=[
                                html.H3("High Risk Orders", style={'fontSize': '18px', 'fontWeight': 'semibold', 'marginBottom': '10px', 'color': '#6c757d'}),
                                html.P(id='high-risk-orders', style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#e74c3c'})
                            ]
                        ),
                        html.Div(
                            style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.12)'},
                            children=[
                                html.H3("Medium Risk Orders", style={'fontSize': '18px', 'fontWeight': 'semibold', 'marginBottom': '10px', 'color': '#6c757d'}),
                                html.P(id='medium-risk-orders', style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#f39c12'})
                            ]
                        ),
                        html.Div(
                            style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.12)'},
                            children=[
                                html.H3("Low Risk Orders", style={'fontSize': '18px', 'fontWeight': 'semibold', 'marginBottom': '10px', 'color': '#6c757d'}),
                                html.P(id='low-risk-orders', style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#2ecc71'})
                            ]
                        ),
                    ]
                ),
                
                # Fraud Detection Section
                html.Div(
                    style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px', 'marginBottom': '20px'},
                    children=[
                        # Anomaly Detection Chart
                        html.Div(
                            style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.12)'},
                            children=[
                                html.H2("Anomaly Detection", style={'fontSize': '20px', 'fontWeight': 'bold', 'marginBottom': '15px', 'color': '#2C3E50'}),
                                html.Div(
                                    style={'height': '250px'},
                                    children=[
                                        html.Div("Order Amount vs. Fraud Score", style={'textAlign': 'center', 'fontSize': '14px', 'color': '#6c757d', 'marginBottom': '10px'}),
                                        dcc.Graph(id='anomaly-scatter', style={'height': '220px'})
                                    ]
                                ),
                                html.Div([
                                    html.H3("Suspicious Orders", style={'fontWeight': 'semibold', 'fontSize': '16px', 'color': '#6c757d', 'marginTop': '10px'}),
                                    html.Div(id='suspicious-orders-list', style={'maxHeight': '120px', 'overflowY': 'auto', 'marginTop': '10px'})
                                ])
                            ]
                        ),
                        
                        # Payment Method Analysis
                        html.Div(
                            style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.12)'},
                            children=[
                                html.H2("Payment Method Analysis", style={'fontSize': '20px', 'fontWeight': 'bold', 'marginBottom': '15px', 'color': '#2C3E50'}),
                                html.Div(
                                    style={'height': '250px'},
                                    children=[
                                        dcc.Graph(id='payment-pie', style={'height': '250px'})
                                    ]
                                ),
                                html.Div([
                                    html.H3("Payment Method Insights", style={'fontWeight': 'semibold', 'fontSize': '16px', 'color': '#6c757d', 'marginTop': '10px'}),
                                    html.P(id='payment-insights', style={'fontSize': '14px', 'color': '#6c757d', 'marginTop': '5px'})
                                ])
                            ]
                        )
                    ]
                ),
                
                # Sentiment and Category Analysis Section
                html.Div(
                    style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px'},
                    children=[
                        # Sentiment Analysis
                        html.Div(
                            style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.12)'},
                            children=[
                                html.H2("Customer Sentiment Analysis", style={'fontSize': '20px', 'fontWeight': 'bold', 'marginBottom': '15px', 'color': '#2C3E50'}),
                                html.Div(
                                    style={'height': '250px'},
                                    children=[
                                        dcc.Graph(id='sentiment-pie', style={'height': '250px'})
                                    ]
                                ),
                                html.Div([
                                    html.H3("Sentiment Insights", style={'fontWeight': 'semibold', 'fontSize': '16px', 'color': '#6c757d', 'marginTop': '10px'}),
                                    html.P(id='sentiment-insights', style={'fontSize': '14px', 'color': '#6c757d', 'marginTop': '5px'})
                                ])
                            ]
                        ),
                        
                        # Fraud by Category
                        html.Div(
                            style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.12)'},
                            children=[
                                html.H2("Average Fraud Score by Category", style={'fontSize': '20px', 'fontWeight': 'bold', 'marginBottom': '15px', 'color': '#2C3E50'}),
                                html.Div(
                                    style={'height': '250px'},
                                    children=[
                                        dcc.Graph(id='category-bar', style={'height': '250px'})
                                    ]
                                ),
                                html.Div([
                                    html.H3("Category Risk Insights", style={'fontWeight': 'semibold', 'fontSize': '16px', 'color': '#6c757d', 'marginTop': '10px'}),
                                    html.P(id='category-insights', style={'fontSize': '14px', 'color': '#6c757d', 'marginTop': '5px'})
                                ])
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# Callback for threshold value display
@app.callback(
    Output('threshold-value', 'children'),
    [Input('fraud-threshold', 'value')]
)
def update_threshold_value(value):
    return f"Current: {value}"

# Filter data based on inputs
def filter_dataframe(category, date_range):
    filtered = df.copy()
    
    # Filter by category
    if category != 'All':
        filtered = filtered[filtered['Product_Category'] == category]
    
    # Filter by date
    if date_range == 'recent':
        filtered = filtered[filtered['IsRecent']]
    elif date_range in ['Jan', 'Feb', 'Mar']:
        filtered = filtered[filtered['Month'] == date_range]
    
    return filtered

# Callbacks for updating all components
@app.callback(
    [Output('total-orders', 'children'),
     Output('high-risk-orders', 'children'),
     Output('medium-risk-orders', 'children'),
     Output('low-risk-orders', 'children'),
     Output('anomaly-scatter', 'figure'),
     Output('suspicious-orders-list', 'children'),
     Output('payment-pie', 'figure'),
     Output('payment-insights', 'children'),
     Output('sentiment-pie', 'figure'),
     Output('sentiment-insights', 'children'),
     Output('category-bar', 'figure'),
     Output('category-insights', 'children')],
    [Input('category-filter', 'value'),
     Input('date-range-filter', 'value'),
     Input('fraud-threshold', 'value')]
)
def update_dashboard(category, date_range, threshold):
    # Filter the data
    filtered_df = filter_dataframe(category, date_range)
    
    # Calculate fraud risk levels
    fraud_levels = calculate_fraud_risk_levels(filtered_df)
    
    # Get anomaly data
    anomalies = get_anomaly_data(filtered_df, threshold)
    
    # Create anomaly scatter plot
    if anomalies.empty:
        scatter_fig = px.scatter(title="No anomalies detected with current filters")
        scatter_fig.update_layout(
            xaxis_title="Order Amount",
            yaxis_title="Fraud Score",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=40, b=40)
        )
        suspicious_orders = html.P("No suspicious orders detected", style={'fontSize': '14px', 'color': '#6c757d'})
    else:
        scatter_fig = px.scatter(
            anomalies, 
            x="Order_Amount", 
            y="Fraudulent_Activity",
            hover_data=["Order_ID", "Product_Category", "Order_Amount"],
            title=f"Orders with Fraud Score ≥ {threshold}"
        )
        scatter_fig.update_layout(
            xaxis_title="Order Amount ($)",
            yaxis_title="Fraud Score",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=40, b=40)
        )
        suspicious_orders = html.Ul([
            html.Li(
                f"Order {row['id_short']}... - ${row['Order_Amount']:.2f} - {row['Product_Category']}",
                style={'marginBottom': '5px', 'paddingBottom': '5px', 'borderBottom': '1px solid #eee', 'fontSize': '14px'}
            ) for _, row in anomalies.iterrows()
        ], style={'listStyleType': 'none', 'padding': '0'})
    
    # Payment method distribution
    payment_counts = get_payment_method_distribution(filtered_df)
    payment_df = pd.DataFrame({
        'Method': list(payment_counts.keys()),
        'Count': list(payment_counts.values())
    })
    
    payment_fig = px.pie(
        payment_df, 
        values='Count', 
        names='Method',
        title="Payment Method Distribution",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    payment_fig.update_layout(
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Payment insights
    if payment_df.empty:
        payment_insight = "No payment data available with current filters."
    else:
        most_common = payment_df.sort_values('Count', ascending=False).iloc[0]['Method']
        high_risk_methods = payment_df[payment_df['Method'].isin(['Gift Card', 'PayPal'])].sort_values('Count', ascending=False)
        
        payment_insight = f"{most_common} is the most common payment method."
        if not high_risk_methods.empty:
            payment_insight += f" {high_risk_methods.iloc[0]['Method']} usage may require additional verification."
    
    # Sentiment analysis
    sentiment_data = get_sentiment_data(filtered_df)
    sentiment_df = pd.DataFrame({
        'Sentiment': ['Positive', 'Neutral', 'Negative'],
        'Count': [sentiment_data['positive'], sentiment_data['neutral'], sentiment_data['negative']],
        'Color': ['#4CAF50', '#FFC107', '#F44336']
    })
    
    sentiment_fig = px.pie(
        sentiment_df, 
        values='Count', 
        names='Sentiment',
        title="Customer Sentiment",
        color='Sentiment',
        color_discrete_map={'Positive': '#4CAF50', 'Neutral': '#FFC107', 'Negative': '#F44336'}
    )
    sentiment_fig.update_layout(
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Sentiment insights
    if sentiment_df['Count'].sum() == 0:
        sentiment_insight = "No sentiment data available with current filters."
    else:
        pos = sentiment_data['positive']
        neg = sentiment_data['negative']
        
        if pos > neg:
            sentiment_insight = "Positive sentiment exceeds negative, suggesting good customer satisfaction."
        elif neg > pos:
            sentiment_insight = "Negative sentiment exceeds positive, suggesting customer satisfaction issues."
        else:
            sentiment_insight = "Balanced sentiment suggests mixed customer experiences."
    
    # Fraud by category
    category_fraud = get_fraud_by_category(filtered_df)
    
    category_fig = px.bar(
        category_fraud, 
        x='Product_Category', 
        y='Fraudulent_Activity',
        title="Average Fraud Score by Category",
        color='Fraudulent_Activity',
        color_continuous_scale='Blues'
    )
    category_fig.update_layout(
        xaxis_title="Product Category",
        yaxis_title="Average Fraud Score",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    # Category insights
    if category_fraud.empty:
        category_insight = "No category data available with current filters."
    else:
        highest_risk = category_fraud.sort_values('Fraudulent_Activity', ascending=False).iloc[0]
        category_insight = f"{highest_risk['Product_Category']} has the highest average fraud score ({highest_risk['Fraudulent_Activity']:.1f}), suggesting increased monitoring may be beneficial."
    
    # Return all updated components
    return (
        len(filtered_df),  # total orders
        fraud_levels['high'],  # high risk
        fraud_levels['medium'],  # medium risk
        fraud_levels['low'],  # low risk
        scatter_fig,  # anomaly scatter
        suspicious_orders,  # suspicious orders list
        payment_fig,  # payment pie
        payment_insight,  # payment insights
        sentiment_fig,  # sentiment pie
        sentiment_insight,  # sentiment insights
        category_fig,  # category bar
        category_insight  # category insights
    )

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)