import mysql.connector

# Connect to MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="15313037S@i",
        database="car_quest250"
    )

# Function to suggest a car based on user input
def suggest_car(price, body_type, fuel_type):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Query to select cars based on user preferences
    query = ("SELECT brand, model, price, car_type FROM cars "
             "WHERE price <= %s AND car_type = %s AND fuel_type = %s")

    cursor.execute(query, (price, body_type, fuel_type))
    cars = cursor.fetchall()

    conn.close()

    if cars:
        # Return the first car from the result set
        return cars[0]
    else:
        return None

# Example usage
price = float(input("Enter your budget: "))
body_type = input("Enter your preferred body type (e.g., sedan, SUV, truck): ")
fuel_type = input("Enter your preferred fuel type (e.g., petrol, diesel, CNG, EV, hybrid): ")

recommended_car = suggest_car(price, body_type, fuel_type)
if recommended_car:
    print(f"We recommend the {recommended_car[0]} {recommended_car[1]} for you.")
else:
    print("Sorry, we couldn't find a car matching your criteria.")
