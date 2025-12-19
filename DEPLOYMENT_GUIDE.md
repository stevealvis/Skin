# Django Skin Disease Prediction App - Deployment Guide

## ✅ Configuration Complete

Your Django application has been prepared for deployment with the following configurations:

### Files Created/Modified:
- ✅ `disease_prediction/settings.py` - Production settings with environment variables
- ✅ `requirements.txt` - Updated with production dependencies
- ✅ `Procfile` - Heroku web process configuration  
- ✅ `runtime.txt` - Python version specification
- ✅ `.env.example` - Environment variables template

### Production Dependencies Added:
- `gunicorn` - WSGI HTTP Server for production
- `whitenoise` - Static file serving for production
- `dj-database-url` - Database URL parsing
- `psycopg2-binary` - PostgreSQL database adapter

## Deployment Options

### Option 1: Heroku CLI (Recommended if CLI available)
```bash
# Install Heroku CLI manually from: https://devcenter.heroku.com/articles/heroku-cli
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
git push heroku main
heroku run python manage.py migrate
```

### Option 2: Heroku Dashboard Deployment
1. Go to [Heroku Dashboard](https://dashboard.heroku.com)
2. Create new app from GitHub repository
3. Add PostgreSQL addon
4. Set environment variables in dashboard
5. Deploy from main branch

### Option 3: Alternative Platforms
- **Railway**: Similar to Heroku, easy deployment
- **Render**: Good free tier, PostgreSQL included
- **DigitalOcean App Platform**: Scalable, database included

## Environment Variables to Set

```bash
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.herokuapp.com,www.your-domain.com
DATABASE_URL=postgresql://user:password@host:port/database
```

## Next Steps After Deployment

1. **Database Setup**: Run migrations
   ```bash
   heroku run python manage.py migrate
   ```

2. **Create Superuser**: 
   ```bash
   heroku run python manage.py createsuperuser
   ```

3. **Collect Static Files**: 
   ```bash
   heroku run python manage.py collectstatic --noinput
   ```

4. **Test Your Application**: Visit your Heroku app URL

## Local Testing Before Deployment

Test your app locally with production settings:
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DEBUG=False
export SECRET_KEY=your-secret-key
export ALLOWED_HOSTS=localhost,127.0.0.1

# Run migrations
python manage.py migrate

# Test server
python manage.py runserver
```

## Troubleshooting

**Static Files Issues**: Ensure Whitenoise is in MIDDLEWARE and STATIC_ROOT is configured
**Database Connection**: Verify DATABASE_URL is correctly set
**Import Errors**: Check all dependencies are in requirements.txt

## Security Checklist

- ✅ SECRET_KEY moved to environment variables
- ✅ DEBUG=False for production
- ✅ ALLOWED_HOSTS configured
- ✅ Database credentials secured
- ✅ Static files configured for production

