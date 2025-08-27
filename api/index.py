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

        db_params = get_db_params()
        if not db_params:
            return jsonify({"error": "Database configuration not available"}), 500
            
        conn = pymysql.connect(**db_params)
        with conn.cursor() as cur:
            query = "SELECT * FROM recommendations WHERE price_range = %s AND fuel_type = %s ORDER BY RAND() LIMIT 1"
            cur.execute(query, (price_range, fuel_type))
            recommendation_data = cur.fetchone()
        
        conn.close()

        if recommendation_data:
            recommendation = recommendation_data['recommendation']
            image_url = recommendation_data['image_url']
            car_specs = {
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
            return jsonify({
                "recommendation": recommendation,
                "image_url": image_url,
                "car_specs": car_specs
            })
        else:
            return jsonify({"recommendation": "No recommendation found.", "image_url": ""}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

# For Vercel serverless deployment
app = app

if __name__ == '__main__':
    app.run(debug=True)
