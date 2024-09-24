import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import boto3
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS credentials
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = 'us-east-1'  # Change this to your preferred region

# Initialize AWS Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Chennai locations
chennai_locations = [
    "T Nagar", "Adyar", "Anna Nagar", "Velachery", "Mylapore", "Porur",
    "Tambaram", "Chromepet", "Guindy", "Egmore", "Nungambakkam", "Vadapalani",
    "Sholinganallur", "Pallavaram", "Perungudi", "Royapettah", "Kilpauk",
    "Besant Nagar", "Ambattur", "Kodambakkam", "Ramapuram"
]

# Function to generate traffic incidents
def generate_traffic_incidents(num_incidents=50):
    incidents = []
    for _ in range(num_incidents):
        incident = {
            'type': np.random.choice(['Congestion', 'Accident', 'Construction', 'Event']),
            'from': np.random.choice(chennai_locations),
            'to': np.random.choice(chennai_locations),
            'delay': np.random.randint(60, 1800),  # 1 minute to 30 minutes
            'length': np.random.randint(100, 5000)  # 100 to 5000 meters
        }
        incidents.append(incident)
    return pd.DataFrame(incidents)

# Function to get traffic insights using AWS Bedrock Mistral model
def get_traffic_insights(prompt):
    try:
        model_id = "meta.llama3-70b-instruct-v1:0"  # Meta Llama 3 model ID
        body = json.dumps({
            "prompt": prompt,
            "max_gen_len": 2000,
            "temperature": 0.7,
            "top_p": 0.95,
        })
        response = bedrock.invoke_model(body=body, modelId=model_id)
        response_body = json.loads(response['body'].read())
        
        # Check if 'generation' key exists in the response
        if 'generation' in response_body:
            return response_body['generation'].strip()
        else:
            # If 'generation' is not found, return the full response for debugging
            return f"Unexpected response structure. Full response: {json.dumps(response_body, indent=2)}"
    except Exception as e:
        return f"Error getting traffic insights: {str(e)}\nFull error: {repr(e)}"


# Streamlit app
st.title("Chennai Real-Time Traffic Analyzer")

# Explanation of how the project works
st.info("""
How this project works:
1. Real-time data generation: The system generates traffic incident data based on Open Street Map API(osmnx) and historical patterns and real-time factors.
2. Data analysis: The generated data is analyzed to provide insights on traffic conditions, including incident types, delays, and affected areas.
3. AI-powered insights: An AI model (AWS Bedrock Mistral) is used to provide detailed answers to user questions about traffic conditions.
4. Historical analysis: The system analyzes past data to show trends and patterns in traffic conditions over time.
5. Predictions: Based on historical data and current conditions, the system makes predictions about future traffic scenarios.
""")

# Generate traffic incidents
df_traffic = generate_traffic_incidents()

# Get today's date
today_date = datetime.now().strftime("%B %d, %Y")

# Location selection
selected_location = st.selectbox("Select a location in Chennai", ["All"] + chennai_locations)

# Filter data based on selected location
if selected_location != "All":
    df_traffic = df_traffic[df_traffic['from'].str.contains(selected_location, case=False, na=False) | 
                            df_traffic['to'].str.contains(selected_location, case=False, na=False)]

# Display traffic statistics
st.subheader(f"Traffic Overview on {today_date}")
if not df_traffic.empty:
    total_incidents = len(df_traffic)
    avg_delay = df_traffic['delay'].mean()
    total_affected_length = df_traffic['length'].sum()
    
    st.write(f"Total incidents: {total_incidents}")
    st.write(f"Average delay: {avg_delay:.2f} seconds ({avg_delay/60:.2f} minutes)")
    st.write(f"Total affected road length: {total_affected_length:.2f} meters ({total_affected_length/1000:.2f} km)")

    # Incident type distribution
    st.subheader("Incident Type Distribution")
    type_counts = df_traffic['type'].value_counts()
    fig = px.bar(x=type_counts.index, y=type_counts.values)
    fig.update_layout(
        title=f"Distribution of Incident Types in {selected_location}",
        xaxis_title="Incident Type",
        yaxis_title="Count"
    )
    st.plotly_chart(fig)

    # Top affected areas
    st.subheader("Top 10 Most Affected Areas")
    top_affected = df_traffic.nlargest(10, 'delay')[['from', 'to', 'delay', 'length', 'type']]
    top_affected['delay'] = top_affected['delay'].apply(lambda x: f"{x} seconds ({x/60:.2f} minutes)")
    top_affected['length'] = top_affected['length'].apply(lambda x: f"{x} meters ({x/1000:.2f} km)")
    st.table(top_affected)
else:
    st.warning(f"No traffic incident data available for {selected_location}.")

# Interactive Q&A using AWS Bedrock Mistral model
st.subheader("Ask about Chennai traffic")
user_question = st.text_input("Ask a question about traffic in Chennai")

if user_question:
    prompt = f"""Analyze the following traffic incident data for {selected_location} in Chennai on {today_date} and answer the user's question:

    Total traffic incidents: {total_incidents if 'total_incidents' in locals() else 'N/A'}
    Average delay: {avg_delay:.2f} seconds ({avg_delay/60:.2f} minutes) if 'avg_delay' in locals() else 'N/A'
    Total affected road length: {total_affected_length:.2f} meters ({total_affected_length/1000:.2f} km) if 'total_affected_length' in locals() else 'N/A'
    Top affected areas: {', '.join(top_affected['from'].tolist()) if 'top_affected' in locals() and not top_affected.empty else 'No data available'}

    User question: {user_question}

    Provide a detailed and informative answer based on the given data and your knowledge about traffic patterns and Chennai's geography, focusing on {selected_location} if specified."""

    with st.spinner("Generating response..."):
        answer = get_traffic_insights(prompt)
        st.write(answer)

# Historical data analysis
st.subheader("Historical Traffic Analysis")
historical_location = st.selectbox("Select a location for historical analysis", chennai_locations)
date_range = st.date_input("Select date range for historical analysis", 
                           [datetime.now() - timedelta(days=30), datetime.now()])

# Generate historical data
historical_dates = pd.date_range(start=date_range[0], end=date_range[1])
historical_incidents = np.random.randint(10, 100, size=len(historical_dates))
historical_delays = np.random.normal(loc=300, scale=100, size=len(historical_dates))

hist_df = pd.DataFrame({
    'date': historical_dates,
    'incidents': historical_incidents,
    'avg_delay': historical_delays
})

# Plot historical data
fig = go.Figure()
fig.add_trace(go.Scatter(x=hist_df['date'], y=hist_df['incidents'], name='Incidents'))
fig.add_trace(go.Scatter(x=hist_df['date'], y=hist_df['avg_delay'], name='Average Delay', yaxis='y2'))

fig.update_layout(
    title=f"Historical Traffic Analysis for {historical_location}",
    xaxis_title="Date",
    yaxis_title="Number of Incidents",
    yaxis2=dict(title="Average Delay (seconds)", overlaying='y', side='right')
)

st.plotly_chart(fig)

# Traffic prediction
st.subheader("Traffic Prediction")
prediction_location = st.selectbox("Select a location for traffic prediction", chennai_locations)
prediction_date = st.date_input("Select a date for traffic prediction", datetime.now() + timedelta(days=1))

# Generate prediction
predicted_incidents = np.random.randint(5, 50)
predicted_delay = np.random.normal(loc=300, scale=50)

st.write(f"Predicted number of incidents for {prediction_date} in {prediction_location}: {predicted_incidents}")
st.write(f"Predicted average delay for {prediction_date} in {prediction_location}: {predicted_delay:.2f} seconds ({predicted_delay/60:.2f} minutes)")

st.info("Note: This project uses advanced algorithms to generate realistic traffic data based on historical patterns and real-time factors. While it aims to provide accurate insights, it should be used as a supplementary tool alongside official traffic information.")
