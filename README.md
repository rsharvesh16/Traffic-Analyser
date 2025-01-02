# Chennai Real-Time Traffic Analyzer

## Overview
The **Chennai Real-Time Traffic Analyzer** is a Streamlit application designed to provide real-time and historical traffic insights for various locations in Chennai. It uses AI-powered insights, data visualization, and predictive modeling to analyze and forecast traffic conditions. The application integrates AWS Bedrock's Mistral model to answer user questions about traffic, making it a powerful tool for traffic monitoring and planning.

---

## Features
1. **Real-Time Traffic Data Generation**:
   - Generates realistic traffic incident data using simulated patterns and factors.
   - Includes incident types like congestion, accidents, construction, and events.

2. **Interactive Traffic Analysis**:
   - Select a location in Chennai to view traffic details.
   - Get statistics such as total incidents, average delay, and affected road length.
   - Visualize incident type distribution and most affected areas.

3. **AI-Powered Q&A**:
   - Ask specific questions about traffic conditions.
   - Powered by the AWS Bedrock Mistral model for detailed insights.

4. **Historical Traffic Analysis**:
   - Analyze traffic patterns for selected locations over a date range.
   - Visualize trends in the number of incidents and average delays.

5. **Traffic Prediction**:
   - Predict future traffic scenarios for selected locations and dates.
   - View anticipated incidents and delays based on historical patterns.


## Customization
- **Chennai Locations**: Modify the `chennai_locations` list to include or remove areas.
- **Data Generation**: Customize `generate_traffic_incidents()` for specific data patterns.
- **Historical Analysis**: Adjust the date range and trends in `historical_analysis`.

---

## Technologies Used
- **Frontend**: Streamlit for interactive web UI.
- **Backend**: AWS Bedrock for AI insights.
- **Data Visualization**: Plotly for charts and graphs.
- **Programming Language**: Python.

---

## Contributing
Contributions are welcome! If you have ideas for new features or optimizations, feel free to submit a pull request or open an issue.

---

## License
This project is licensed under the MIT License.

---
