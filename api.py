from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

CSV_FILE_PATH = '/Users/dontizi/Downloads/tailwindui-salient/salient-ts/sorted.csv'
COLUMN_HEADERS = ['start_time', 'end_time', 'vehicle_class', 'station']

# Define service time and price for each vehicle type
SERVICE_INFO = {
    'compact': {'time': 30, 'price': 150},
    'medium': {'time': 30, 'price': 150},
    'full-size': {'time': 30, 'price': 150},
    'class 1 truck': {'time': 60, 'price': 700},
    'class 2 truck': {'time': 120, 'price': 700}
}

# In-memory storage for scheduling (for demonstration purposes)
schedules = {vehicle_class: [] for vehicle_class in SERVICE_INFO.keys()}

def add_price_column(df, vehicle_class_col):
    df['price'] = df[vehicle_class_col].apply(lambda x: SERVICE_INFO[x]['price'])
    return df

def filter_by_time(df, end_time_col):
    df[end_time_col] = pd.to_datetime(df[end_time_col])
    return df[df[end_time_col].dt.hour.between(7, 19)]

def is_slot_available(vehicle_class, start_time, end_time):
    for booking in schedules[vehicle_class]:
        if start_time < booking['end_time'] and end_time > booking['start_time']:
            return False
    return True

def book_slot(vehicle_class, start_time, end_time):
    schedules[vehicle_class].append({'start_time': start_time, 'end_time': end_time})

@app.route('/schedule', methods=['POST'])
def schedule_service():
    data = request.json
    vehicle_class = data['vehicle_class']
    start_time_str = data['start_time']
    end_time_str = data['end_time']
    
    requested_start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    requested_end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')

    service_duration = timedelta(minutes=SERVICE_INFO[vehicle_class]['time'])
    end_time = requested_start_time + service_duration

    if is_slot_available(vehicle_class, requested_start_time, end_time):
        book_slot(vehicle_class, requested_start_time, end_time)
        return jsonify({"message": "Service scheduled", "start_time": requested_start_time, "end_time": end_time}), 200
    else:
        return jsonify({"message": "No available slot"}), 409

@app.route('/transactions', methods=['GET', 'POST'])
def get_transactions():
    date_query = request.args.get('date', '')
    df = pd.read_csv(CSV_FILE_PATH, names=COLUMN_HEADERS, header=None)
    df = add_price_column(df, 'vehicle_class')
    df = filter_by_time(df, 'end_time')

    # Filter the DataFrame for transactions that match the specified start date
    filtered_data = df[df['start_time'].str.contains(date_query)]
    
    # Convert the filtered DataFrame to a list of dictionaries for JSON serialization
    transactions_list = filtered_data.to_dict('records')
    return jsonify(transactions_list)

if __name__ == '__main__':
    app.run(debug=True)
