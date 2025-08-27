# Car Quest - Vercel Deployment Guide

## Database Configuration

Your Car Quest app is configured to use your MySQL database:
- **Database**: car_quest250
- **User**: root
- **Password**: 15313037S@i

## For Vercel Deployment

Since Vercel can't access "localhost", you'll need a cloud database. Options:

### Option 1: PlanetScale (Recommended - Free Tier)
1. Go to [planetscale.com](https://planetscale.com)
2. Create free account
3. Create new database: `car_quest250`
4. Copy connection string
5. Add to Vercel environment variables

### Option 2: Railway (Free Tier)
1. Go to [railway.app](https://railway.app)
2. Create MySQL database
3. Copy connection details
4. Add to Vercel environment variables

### Option 3: Aiven (Free Tier)
1. Go to [aiven.io](https://aiven.io)
2. Create MySQL service
3. Import your data
4. Copy connection details

## Vercel Environment Variables

Add these in your Vercel project dashboard:

```
MYSQL_HOST=your_cloud_database_host
MYSQL_USER=your_database_username
MYSQL_PASSWORD=your_database_password
MYSQL_DB=car_quest250
MYSQL_PORT=3306
```

## Database Table Structure

Your app expects a `recommendations` table with these columns:
- id
- price_range
- fuel_type
- recommendation
- image_url
- mileage_arai
- engine_displacement
- max_power
- max_torque
- length
- width
- height
- ground_clearance
- boot_space

## Testing

1. **Local**: Visit `/test-db` to test database connection
2. **Production**: Visit `your-vercel-url/test-db` to verify deployment

## Current Status

✅ App configured to use your database
✅ Database credentials embedded (for local development)
⚠️ Need cloud database for Vercel deployment
