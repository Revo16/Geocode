from flask import Flask, render_template, request
from geopy.geocoders import Nominatim

app = Flask(__name__)
geolocator = Nominatim(user_agent="http")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_coordinates():
    coordinates_input = request.form['coordinates']
    coordinates_list = [tuple(map(float, pair.split(','))) for pair in coordinates_input.split('\n')]

    results = []
    for coordinate in coordinates_list:
        latitude, longitude = coordinate
        location = geolocator.reverse(f"{latitude},{longitude}")
        address = location.raw['address']

        city = address.get('city', '')
        county = address.get('county', '')
        state = address.get('state', '')
        country = address.get('country', '')
        zipcode = address.get('postcode', '')

        results.append({
            'latitude': latitude,
            'longitude': longitude,
            'city': city,
            'county': county,
            'state': state,
            'country': country,
            'zipcode': zipcode,
            'raw_address': address,
        })

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
