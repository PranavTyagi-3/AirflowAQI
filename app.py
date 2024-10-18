from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['airquality']
collection = db['stations']

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    locations_by_time = {}

    # Fetch all unique timestamps from the data
    unique_times = set()
    for post in collection.find():
        for data in db[str(post['uid'])].find():
            unique_times.add(data['time'])

    # Sort timestamps for proper order
    unique_times = sorted(unique_times)

    # Organize data by time and location
    for time in unique_times:
        locations_by_time[time] = {}
        for post in collection.find():
            uid = post['uid']
            # Get the AQI data for this specific time and uid
            data = db[str(uid)].find_one({'time': time})
            if data:
                locations_by_time[time][uid] = {
                    'lat': post['lat'],
                    'lng': post['lon'],
                    'aqi': data['aqi'],
                    'time': time
                }
    # print(locations_by_time)
    # Pass this new structure to the frontend
    return render_template('index.html', stations=locations_by_time, date_len = len(locations_by_time))

if __name__ == '__main__':
    app.run(debug=True)