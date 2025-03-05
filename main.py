from flask import Flask, render_template, jsonify, request
import pymysql
import os

app = Flask(__name__)

db_params = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DB"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "cursorclass": pymysql.cursors.DictCursor,
    "ssl": {"ca": os.getenv("MYSQL_SSL_CA")} if os.getenv("MYSQL_SSL_CA") else None,
}

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/fetch_recommendation')
def fetch_recommendation():
    try:
        price = request.args.get('price', type=int)
        fuel_type = request.args.get('fuelType')

        if price is None or fuel_type is None:
            return jsonify({"error": "Missing parameters"}), 400

        if price < 600000:
            price_range = 'Budget'
        elif price < 900000:
            price_range = 'Mid-range'
        elif price < 1500000:
            price_range = 'High-mid range'
        elif price < 1900000:
            price_range = 'Upper-mid range'
        elif price < 4200000:
            price_range = 'Upper-mid-high range'
        elif price < 5500000:
            price_range = 'Luxury'
        elif price < 7000000:
            price_range = 'Ultra Luxury'
        elif price < 10000000:
            price_range = 'Premium Luxury'
        elif price < 25000000:
            price_range = 'Super Premium Luxury'
        elif price < 50000000:
            price_range = 'Super Deluxe Luxury'
        else:
            price_range = 'Beyond Luxury'

        conn = pymysql.connect(**db_params)
        with conn.cursor() as cur:
            query = "SELECT * FROM recommendations WHERE price_range = %s AND fuel_type = %s ORDER BY RAND() LIMIT 1"
            cur.execute(query, (price_range, fuel_type))
            recommendation_data = cur.fetchone()

        conn.close()

        if recommendation_data:
            return jsonify({
                "recommendation": recommendation_data['recommendation'],
                "image_url": recommendation_data['image_url'],
                "car_specs": {
                    "mileage_arai": recommendation_data['mileage_arai'],
                    "engine_displacement": recommendation_data['engine_displacement'],
                    "max_power": recommendation_data['max_power'],
                    "max_torque": recommendation_data['max_torque'],
                    "length": recommendation_data['length'],
                    "width": recommendation_data['width'],
                    "height": recommendation_data['height'],
                    "ground_clearance": recommendation_data['ground_clearance'],
                    "boot_space": recommendation_data['boot_space']
                }
            })
        else:
            return jsonify({"recommendation": "No recommendation found.", "image_url": ""}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
