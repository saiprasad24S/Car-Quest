from flask import Flask, render_template, jsonify, request
import pymysql
import os

app = Flask(__name__, template_folder='../templates')

# Database configuration with error handling
def get_db_params():
    # Use environment variables if available, otherwise use defaults
    return {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", "15313037S@i"),
        "database": os.getenv("MYSQL_DB", "car_quest250"),
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

@app.route('/test-db')
def test_db():
    """Test database connection and show table structure"""
    db_params = get_db_params()
    
    try:
        conn = pymysql.connect(**db_params)
        
        with conn.cursor() as cur:
            # Test connection
            cur.execute("SELECT 1")
            
            # Show tables
            cur.execute("SHOW TABLES")
            tables = cur.fetchall()
            
            # Check recommendations table structure
            cur.execute("DESCRIBE recommendations")
            table_structure = cur.fetchall()
            
            # Count recommendations
            cur.execute("SELECT COUNT(*) as count FROM recommendations")
            count_result = cur.fetchone()
            
            # Sample data
            cur.execute("SELECT price_range, fuel_type, recommendation FROM recommendations LIMIT 5")
            sample_data = cur.fetchall()
            
        conn.close()
        
        return jsonify({
            "status": "success",
            "message": "Database connection successful",
            "database_info": {
                "host": db_params['host'],
                "database": db_params['database'],
                "tables": tables,
                "recommendations_count": count_result['count'],
                "table_structure": table_structure,
                "sample_data": sample_data
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Database connection failed: {str(e)}",
            "connection_params": {
                "host": db_params.get('host', 'Not set'),
                "database": db_params.get('database', 'Not set'),
                "user": db_params.get('user', 'Not set')
            }
        })

# Mock data for demonstration when database is unavailable
mock_recommendations = {
    # Budget Range (< 600,000)
    "Budget_Petrol": {
        "recommendation": "Maruti Suzuki Alto K10 - Perfect budget car with excellent fuel efficiency",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/130583/alto-k10-exterior-right-front-three-quarter-109.jpeg",
        "mileage_arai": "24.39 kmpl", "engine_displacement": "998 cc", "max_power": "66.95 bhp", "max_torque": "89 Nm",
        "length": "3530 mm", "width": "1490 mm", "height": "1520 mm", "ground_clearance": "160 mm", "boot_space": "214 L"
    },
    
    # Mid-range (600,000 - 900,000)
    "Mid-range_Petrol": {
        "recommendation": "Hyundai i20 - Feature-rich mid-range hatchback with premium feel",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/106815/i20-exterior-right-front-three-quarter-4.jpeg",
        "mileage_arai": "20.35 kmpl", "engine_displacement": "1197 cc", "max_power": "82.85 bhp", "max_torque": "113.8 Nm",
        "length": "3995 mm", "width": "1775 mm", "height": "1505 mm", "ground_clearance": "165 mm", "boot_space": "311 L"
    },
    "Mid-range_Diesel": {
        "recommendation": "Maruti Suzuki Baleno Diesel - Fuel efficient and spacious",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/40432/baleno-exterior-right-front-three-quarter-11.jpeg",
        "mileage_arai": "23.87 kmpl", "engine_displacement": "1248 cc", "max_power": "89.76 bhp", "max_torque": "200 Nm",
        "length": "3990 mm", "width": "1745 mm", "height": "1500 mm", "ground_clearance": "170 mm", "boot_space": "339 L"
    },
    
    # High-mid range (900,000 - 1,500,000)
    "High-mid range_Petrol": {
        "recommendation": "Hyundai Creta - Popular compact SUV with great features",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/106843/creta-exterior-right-front-three-quarter-4.jpeg",
        "mileage_arai": "17.4 kmpl", "engine_displacement": "1497 cc", "max_power": "113.4 bhp", "max_torque": "144 Nm",
        "length": "4300 mm", "width": "1790 mm", "height": "1635 mm", "ground_clearance": "190 mm", "boot_space": "433 L"
    },
    "High-mid range_Diesel": {
        "recommendation": "Kia Seltos Diesel - Stylish SUV with powerful engine",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115777/seltos-exterior-right-front-three-quarter-73.jpeg",
        "mileage_arai": "20.0 kmpl", "engine_displacement": "1493 cc", "max_power": "113.4 bhp", "max_torque": "250 Nm",
        "length": "4315 mm", "width": "1800 mm", "height": "1645 mm", "ground_clearance": "190 mm", "boot_space": "433 L"
    },
    
    # Upper-mid range (1,500,000 - 1,900,000)
    "Upper-mid range_Petrol": {
        "recommendation": "Honda City - Premium sedan with excellent build quality",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/134287/city-exterior-right-front-three-quarter-76.jpeg",
        "mileage_arai": "17.8 kmpl", "engine_displacement": "1498 cc", "max_power": "119.35 bhp", "max_torque": "145 Nm",
        "length": "4549 mm", "width": "1748 mm", "height": "1489 mm", "ground_clearance": "165 mm", "boot_space": "506 L"
    },
    "Upper-mid range_Diesel": {
        "recommendation": "Volkswagen Virtus Diesel - German engineering excellence",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/144681/virtus-exterior-right-front-three-quarter-4.jpeg",
        "mileage_arai": "21.5 kmpl", "engine_displacement": "1498 cc", "max_power": "108.62 bhp", "max_torque": "250 Nm",
        "length": "4561 mm", "width": "1752 mm", "height": "1507 mm", "ground_clearance": "179 mm", "boot_space": "521 L"
    },
    
    # Upper-mid-high range (1,900,000 - 4,200,000)
    "Upper-mid-high range_Petrol": {
        "recommendation": "Toyota Camry - Reliable luxury sedan with hybrid technology",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/51909/camry-exterior-right-front-three-quarter-2.jpeg",
        "mileage_arai": "23.33 kmpl", "engine_displacement": "2487 cc", "max_power": "176.31 bhp", "max_torque": "221 Nm",
        "length": "4885 mm", "width": "1840 mm", "height": "1455 mm", "ground_clearance": "160 mm", "boot_space": "621 L"
    },
    "Upper-mid-high range_Hybrid": {
        "recommendation": "Toyota Camry Hybrid - Eco-friendly luxury with exceptional mileage",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/51909/camry-exterior-right-front-three-quarter-2.jpeg",
        "mileage_arai": "23.33 kmpl", "engine_displacement": "2487 cc", "max_power": "215 bhp", "max_torque": "221 Nm",
        "length": "4885 mm", "width": "1840 mm", "height": "1455 mm", "ground_clearance": "160 mm", "boot_space": "621 L"
    },
    
    # Luxury (4,200,000 - 5,500,000)
    "Luxury_Petrol": {
        "recommendation": "BMW 3 Series - Premium luxury sedan with excellent performance",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115025/3-series-exterior-right-front-three-quarter-4.jpeg",
        "mileage_arai": "16.13 kmpl", "engine_displacement": "1998 cc", "max_power": "255.02 bhp", "max_torque": "400 Nm",
        "length": "4709 mm", "width": "1827 mm", "height": "1442 mm", "ground_clearance": "140 mm", "boot_space": "480 L"
    },
    "Luxury_Diesel": {
        "recommendation": "Mercedes-Benz C-Class Diesel - Luxury with efficiency",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/130591/c-class-exterior-right-front-three-quarter-109.jpeg",
        "mileage_arai": "17.2 kmpl", "engine_displacement": "1993 cc", "max_power": "194 bhp", "max_torque": "400 Nm",
        "length": "4751 mm", "width": "1820 mm", "height": "1437 mm", "ground_clearance": "133 mm", "boot_space": "455 L"
    },
    
    # EV Options
    "Mid-range_EV": {
        "recommendation": "Tata Nexon EV - India's popular electric SUV",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/141867/nexon-ev-exterior-right-front-three-quarter-71.jpeg",
        "mileage_arai": "312 km range", "engine_displacement": "Electric Motor", "max_power": "141 bhp", "max_torque": "250 Nm",
        "length": "3993 mm", "width": "1811 mm", "height": "1606 mm", "ground_clearance": "209 mm", "boot_space": "350 L"
    },
    "High-mid range_EV": {
        "recommendation": "MG ZS EV - Feature-loaded electric SUV",
        "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/130629/zs-ev-exterior-right-front-three-quarter-109.jpeg",
        "mileage_arai": "419 km range", "engine_displacement": "Electric Motor", "max_power": "176 bhp", "max_torque": "280 Nm",
        "length": "4323 mm", "width": "1809 mm", "height": "1649 mm", "ground_clearance": "161 mm", "boot_space": "448 L"
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

        # Database connection - prioritize database over mock data
        db_params = get_db_params()
        
        if not db_params:
            return jsonify({
                "error": "Database not configured. Please set environment variables: MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB"
            }), 500
            
        try:
            # Connect to database
            conn = pymysql.connect(**db_params)
            print(f"Successfully connected to database: {db_params['host']}")
            
            with conn.cursor() as cur:
                # Query database for recommendations
                query = "SELECT * FROM recommendations WHERE price_range = %s AND fuel_type = %s ORDER BY RAND() LIMIT 1"
                print(f"Executing query: {query} with params: ({price_range}, {fuel_type})")
                cur.execute(query, (price_range, fuel_type))
                recommendation_data = cur.fetchone()
                
                if recommendation_data:
                    print(f"Found recommendation: {recommendation_data['recommendation'][:50]}...")
                    conn.close()
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
                    print(f"No recommendations found for {price_range} + {fuel_type}")
                    conn.close()
                    return jsonify({"recommendation": "No car recommendations found for your criteria.", "image_url": ""}), 200
                    
        except pymysql.Error as db_error:
            print(f"Database connection error: {db_error}")
            return jsonify({
                "error": f"Database connection failed: {str(db_error)}"
            }), 500
            
        except Exception as e:
            print(f"Unexpected database error: {e}")
            return jsonify({
                "error": f"Database error: {str(e)}"
            }), 500
        
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# Vercel needs to find 'app' variable
# This exports the Flask app for Vercel
app = app

if __name__ == '__main__':
    app.run(debug=True)
