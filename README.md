# Car Quest - Car Recommendation System

A Flask-based web application that provides personalized car recommendations based on user preferences like budget and fuel type.

## Features

- Car recommendations based on price range and fuel type
- Interactive web interface with Bootstrap styling
- MySQL database integration for storing car data
- Responsive design with car-themed UI

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Deployment**: Vercel (Serverless)

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables by copying `.env.example` to `.env` and updating the values:
   ```bash
   cp .env.example .env
   ```

3. Configure your MySQL database and update the `.env` file with your database credentials.

4. Run the application:
   ```bash
   python test.py
   ```

## Deployment on Vercel

### Method 1: Using Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy the project:
   ```bash
   vercel
   ```

4. Set up environment variables in Vercel dashboard:
   - Go to your project in Vercel dashboard
   - Navigate to Settings > Environment Variables
   - Add the following variables:
     - `MYSQL_HOST`: Your MySQL host
     - `MYSQL_USER`: Your MySQL username
     - `MYSQL_PASSWORD`: Your MySQL password
     - `MYSQL_DB`: Your database name

### Method 2: Using GitHub Integration

1. Push your code to a GitHub repository
2. Connect your GitHub account to Vercel
3. Import the repository in Vercel
4. Set up environment variables in the Vercel dashboard
5. Deploy automatically

## Database Setup

Your MySQL database should have a `recommendations` table with the following structure:
- `price_range` (VARCHAR)
- `fuel_type` (VARCHAR)
- `recommendation` (TEXT)
- `image_url` (VARCHAR)
- `mileage_arai` (VARCHAR)
- `engine_displacement` (VARCHAR)
- `max_power` (VARCHAR)
- `max_torque` (VARCHAR)
- `length` (VARCHAR)
- `width` (VARCHAR)
- `height` (VARCHAR)
- `ground_clearance` (VARCHAR)
- `boot_space` (VARCHAR)

## Environment Variables

Create a `.env` file with the following variables:

```
MYSQL_HOST=your_mysql_host
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=your_database_name
```

## Project Structure

```
Car Quest/
├── api/
│   └── index.py          # Main Flask application (serverless function)
├── templates/
│   ├── car.html         # Main page
│   ├── about_us.html    # About page
│   └── contact_us.html  # Contact page
├── requirements.txt     # Python dependencies
├── vercel.json         # Vercel configuration
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Important Notes

- The original `test.py` file has been restructured for serverless deployment
- Database credentials should be stored as environment variables for security
- The application uses serverless functions on Vercel, so traditional Flask hosting methods won't work
- Make sure your MySQL database is accessible from the internet for Vercel deployment
