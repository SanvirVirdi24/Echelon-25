import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

def main():
    st.set_page_config(layout="wide", page_title="Clothing Sales Dashboard")
    st.title("Clothing Sales Dashboard")
    
    # CSV Data
    csv_data = """Customer_ID,Customer_Location,Product_ID,Product_Category,Order_ID,Order_Date,Order_Amount,Payment_Method,Discount_Applied,Order_Status,Orders_Replaced,Return_Reason,Device_Used,Browsing_Time,Fraudulent_Activity
ae480c1c-9745-4d76-93ac-346ef28ddb26,Christopherland,d5e29dd8-9f1d-4f50-86c4-75a01c459f76,Sweaters,992df5e1-c6f2-4e0d-b871-ec48402d8b81,19-02-2025,64.9,PayPal,7.19,Returned,1,Size Issue,Mobile,18.43,8
ed203761-7216-450c-a188-ab5a912fb354,Jordanton,fc7c034d-272e-4877-a1e1-90b798608a96,Shoes,1fff79d3-ad16-420e-b2c2-ff3c862c5d9b,06-03-2025,138.29,Gift Card,23.3,Returned,1,Defect,Mobile,13.68,8
039f040e-a848-4c4e-b83c-9b18e40a9fc7,Laurenfurt,c9c3e5d5-854e-4917-96e0-c7c9f9dc1d0b,Shoes,dde25f35-aadf-4643-bd83-607300a79294,28-01-2025,62.21,Debit Card,11.99,Pending,0,N/A,Tablet,28.52,6
a756821b-17a4-4fdf-a4c0-73aea88b3432,South Catherine,238c92da-48d3-4edf-b38f-e0ed9ce1aab9,T-Shirts,124b2170-1365-4b43-9baa-236081055458,05-03-2025,345.45,COD,18.82,Completed,0,N/A,Tablet,27.18,8
deb0ea59-779b-45de-8e37-d4cc3d5b8410,Melindaberg,6ffee7d4-b94b-4e97-a6f9-2b51774d71cc,T-Shirts,d306389f-f04e-423a-8218-315854804ed9,04-02-2025,179,Credit Card,8.97,Completed,0,N/A,Desktop,17.65,3
ebae3c55-bf65-46f0-8183-f63f6faf860a,Wagnerport,1687d42f-6ea5-400d-a126-a18ba543ee83,T-Shirts,e66b0663-44b1-4540-8940-268d7ec1fd17,30-01-2025,424.2,Debit Card,17.17,Cancelled,0,N/A,Tablet,4.12,4
f25a88f4-a307-4247-920f-eaac9b7562d3,Melissafort,22db8ff9-5cba-491e-b4a5-e308ef14d37f,Dresses,82884b21-5f08-4621-9bba-ed83c7cc3c1c,15-02-2025,49.88,Gift Card,1.93,Returned,0,Late Delivery,Tablet,11.09,2
ed6752bd-6d76-4ce8-9cb4-ac613a0d24b2,Frostmouth,9fed6665-881a-45f7-af7c-edf2157434a5,Dresses,383bddcf-28d1-4af9-bdac-353cb3fba7a3,02-01-2025,65.11,COD,27.42,Cancelled,0,N/A,Desktop,28.76,10
77f789b4-8d00-4f66-8999-674075072ce1,North Codymouth,b767abda-7e93-4a9c-970c-34a9baea4482,Shoes,c810f1a7-769d-4d35-bfeb-67ae8f97ec3d,11-01-2025,228.86,COD,27.58,Returned,0,Defect,Tablet,19.15,3
6ca6e84e-3212-4fa3-aa5c-097546a5057a,Phillipside,da87c035-c5d7-49c5-80b1-bb9980d23c00,Jeans,6dd2d1e4-8715-4a57-a21c-4c7296f00cbc,10-01-2025,367.5,PayPal,1.72,Pending,0,N/A,Tablet,20.1,7
52c6c2a5-2c2e-4e80-84f3-b998c359b9dd,Jimenezside,a5a1ece5-7a09-417b-9846-7eabcb924f84,Sweaters,b6352314-47dc-43a5-b04a-8581600c50dd,23-01-2025,480.55,Gift Card,15.51,Completed,0,N/A,Mobile,27.21,3
26e4cf73-19c3-4564-a345-f20eea3da637,Colestad,8f88602e-e80b-420b-b922-e42c3c5045a6,Sweaters,7384c00c-d9b7-44f2-a6b4-f483310312a2,26-01-2025,52.42,Debit Card,28.3,Pending,0,N/A,Tablet,16.39,2
b62be570-7d35-4054-8844-5d72f429bcd7,Christinehaven,d367ee82-143d-491b-8566-6b699d2549c5,Shoes,998a816f-9d6c-48cf-80e8-eed61ec71f20,21-02-2025,255.52,Gift Card,8.81,Pending,0,N/A,Mobile,16.47,10
c3078319-7b37-4c75-bf09-4309e7e35d26,North Karen,514e7244-1101-4c45-ad90-d8a18542ece1,Dresses,57462c4b-1943-4d9e-ace7-902ff01be9e0,19-02-2025,362.03,PayPal,15.43,Completed,0,N/A,Tablet,23.3,2
335fdf70-77db-43d0-9ae6-fc6e265cb80f,West Douglastown,3c50a8aa-89fe-41e6-b677-ba170b6f0d07,T-Shirts,6559a411-ed8a-4742-af53-920d17899620,05-01-2025,419,Debit Card,0.26,Returned,2,Other,Mobile,29.45,3"""
    
    # Parse the CSV data
    data = pd.read_csv(io.StringIO(csv_data))
    
    # Convert Order_Date to datetime
    data['Order_Date'] = pd.to_datetime(data['Order_Date'], format='%d-%m-%Y')
    
    # Sidebar for filters
    st.sidebar.title("Filters")
    
    # Get unique values for filters
    categories = ['All'] + list(data['Product_Category'].unique())
    statuses = ['All'] + list(data['Order_Status'].unique())
    devices = ['All'] + list(data['Device_Used'].unique())
    
    # Date range
    min_date = data['Order_Date'].min().date()
    max_date = data['Order_Date'].max().date()
    
    # Create filters
    category_filter = st.sidebar.selectbox("Product Category", categories)
    status_filter = st.sidebar.selectbox("Order Status", statuses)
    device_filter = st.sidebar.selectbox("Device Used", devices)
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Apply filters
    filtered_data = data.copy()
    
    if category_filter != 'All':
        filtered_data = filtered_data[filtered_data['Product_Category'] == category_filter]
    
    if status_filter != 'All':
        filtered_data = filtered_data[filtered_data['Order_Status'] == status_filter]
    
    if device_filter != 'All':
        filtered_data = filtered_data[filtered_data['Device_Used'] == device_filter]
    
    # Apply date range filter if both start and end dates are selected
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_data = filtered_data[(filtered_data['Order_Date'].dt.date >= start_date) & 
                                     (filtered_data['Order_Date'].dt.date <= end_date)]
    
    # KPI metrics
    total_sales = filtered_data['Order_Amount'].sum()
    avg_order_value = filtered_data['Order_Amount'].mean() if len(filtered_data) > 0 else 0
    total_orders = len(filtered_data)
    
    # Display KPI metrics in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", f"${total_sales:.2f}")
    with col2:
        st.metric("Average Order Value", f"${avg_order_value:.2f}")
    with col3:
        st.metric("Total Orders", total_orders)
    
    # Create charts
    st.subheader("Sales Analysis")
    
    # Prepare data for charts
    category_data = filtered_data.groupby('Product_Category').agg({
        'Order_Amount': 'sum',
        'Order_ID': 'count'
    }).reset_index().rename(columns={'Order_ID': 'Count'})
    
    status_data = filtered_data.groupby('Order_Status').size().reset_index(name='Count')
    payment_data = filtered_data.groupby('Payment_Method').size().reset_index(name='Count')
    
    # Prepare date data
    date_data = filtered_data.groupby(filtered_data['Order_Date'].dt.date).agg({
        'Order_Amount': 'sum',
        'Order_ID': 'count'
    }).reset_index().rename(columns={'Order_ID': 'Count'})
    date_data = date_data.sort_values('Order_Date')
    
    # Charts in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by Category
        fig_category = px.bar(
            category_data, 
            x='Product_Category', 
            y='Order_Amount',
            title='Sales by Category',
            labels={'Product_Category': 'Product Category', 'Order_Amount': 'Sales ($)'}
        )
        st.plotly_chart(fig_category, use_container_width=True)
        
        # Sales Trend
        fig_trend = px.line(
            date_data, 
            x='Order_Date', 
            y='Order_Amount',
            title='Sales Trend',
            labels={'Order_Date': 'Date', 'Order_Amount': 'Sales ($)'}
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        # Order Status Distribution
        fig_status = px.pie(
            status_data, 
            names='Order_Status', 
            values='Count',
            title='Order Status Distribution'
        )
        st.plotly_chart(fig_status, use_container_width=True)
        
        # Payment Method Distribution
        fig_payment = px.pie(
            payment_data, 
            names='Payment_Method', 
            values='Count',
            title='Payment Method Distribution'
        )
        st.plotly_chart(fig_payment, use_container_width=True)
    
    # Recent Orders Table
    st.subheader("Recent Orders")
    
    # Format the Order_Date column for display
    display_data = filtered_data.copy()
    display_data['Order_Date'] = display_data['Order_Date'].dt.strftime('%d-%m-%Y')
    
    # Add color-coding for status
    def highlight_status(s):
        if s == 'Completed':
            return 'background-color: #d4edda; color: #155724'
        elif s == 'Pending':
            return 'background-color: #fff3cd; color: #856404'
        elif s == 'Cancelled':
            return 'background-color: #f8d7da; color: #721c24'
        else:  # Returned
            return 'background-color: #d1ecf1; color: #0c5460'
    
    # Select and order columns for display
    table_data = display_data[['Order_Date', 'Product_Category', 'Order_Amount', 'Order_Status', 'Payment_Method']]
    table_data = table_data.sort_values('Order_Date', ascending=False).head(10)
    
    # Format Order_Amount as currency
    table_data['Order_Amount'] = table_data['Order_Amount'].apply(lambda x: f"${x:.2f}")
    
    # Display the table
    st.dataframe(table_data.style.applymap(highlight_status, subset=['Order_Status']), use_container_width=True)

if __name__ == "__main__":
    main()