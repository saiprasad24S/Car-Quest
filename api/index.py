from flask import Flask, render_template, jsonify, request
import pymysql
import os

app = Flask(__name__, template_folder='../templates')

# Database configuration with error handling
def get_db_params():
    required_env_vars = ["MYSQL_HOST", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DB"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing environment variables: {missing_vars}")
        return None
    
    return {
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
    return render_template('car.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "service": "Car Quest",
        "database_configured": get_db_params() is not None
    })

@app.route('/api/status')
def api_status():
    return jsonify({"message": "Car Quest API is running!", "version": "1.0"})

# Mock data for demonstration when database is unavailable
mock_recommendations = {
    "Budget_Petrol": {
        "recommendation": "Maruti Suzuki Alto K10 - Perfect budget car with excellent fuel efficiency",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/130583/alto-k10-exterior-right-front-three-quarter-109.jpeg",
        "mileage_arai": "24.39 kmpl",
        "engine_displacement": "998 cc",
        "max_power": "66.95 bhp",
        "max_torque": "89 Nm",
        "length": "3530 mm",
        "width": "1490 mm",
        "height": "1520 mm",
        "ground_clearance": "160 mm",
        "boot_space": "214 L"
    },
    "Mid-range_Petrol": {
        "recommendation": "Hyundai i20 - Feature-rich mid-range hatchback with premium feel",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/106815/i20-exterior-right-front-three-quarter-4.jpeg",
        "mileage_arai": "20.35 kmpl",
        "engine_displacement": "1197 cc",
        "max_power": "82.85 bhp",
        "max_torque": "113.8 Nm",
        "length": "3995 mm",
        "width": "1775 mm",
        "height": "1505 mm",
        "ground_clearance": "165 mm",
        "boot_space": "311 L"
    },
    "Luxury_Petrol": {
        "recommendation": "BMW 3 Series - Premium luxury sedan with excellent performance",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115025/3-series-exterior-right-front-three-quarter-4.jpeg",
        "mileage_arai": "16.13 kmpl",
        "engine_displacement": "1998 cc",
        "max_power": "255.02 bhp",
        "max_torque": "400 Nm",
        "length": "4709 mm",
        "width": "1827 mm",
        "height": "1442 mm",
        "ground_clearance": "140 mm",
        "boot_space": "480 L"
    }
}

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

        # Try database first, fallback to mock data
        db_params = get_db_params()
        if db_params:
            try:
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
            except Exception as db_error:
                print(f"Database error: {db_error}")
                # Continue to mock data fallback
        
        # Fallback to mock data when database is unavailable
        mock_key = f"{price_range}_{fuel_type}"
        
        # Use available mock data or default
        if mock_key in mock_recommendations:
            mock_data = mock_recommendations[mock_key]
        else:
            # Use a default recommendation
            mock_data = mock_recommendations["Mid-range_Petrol"]
            mock_data["recommendation"] = f"Recommended car for {price_range} range with {fuel_type} fuel (Demo data - Database not configured)"
        
        return jsonify({
            "recommendation": mock_data["recommendation"],
            "image_url": mock_data["image_url"],
            "car_specs": {
                "mileage_arai": mock_data["mileage_arai"],
                "engine_displacement": mock_data["engine_displacement"],
                "max_power": mock_data["max_power"],
                "max_torque": mock_data["max_torque"],
                "length": mock_data["length"],
                "width": mock_data["width"],
                "height": mock_data["height"],
                "ground_clearance": mock_data["ground_clearance"],
                "boot_space": mock_data["boot_space"]
            }
        })
        
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# Vercel needs to find 'app' variable
# This exports the Flask app for Vercel
app = app

if __name__ == '__main__':
    app.run(debug=True)
