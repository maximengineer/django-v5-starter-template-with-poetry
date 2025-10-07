# Local Settings Directory

This directory is reserved for **local development overrides** and **generated files** that should never be committed to git.

**⚠️ IMPORTANT:** Files in this directory should **NEVER** be committed to git (they're in `.gitignore`).

---

## What Goes Here

### Development Files
- Local database files (SQLite)
- Generated configuration files
- Developer-specific overrides

### Production Files (Not Committed)
- Environment-specific settings loaded via `.env`
- Local media uploads (in development)
- Cache files

---

## Settings Architecture

This project uses a simple, standard Django settings structure:

```
core/backend/settings/
├── __init__.py          # Router based on DJANGO_ENV
├── base.py              # Common settings for all environments
├── dev.py               # Development settings
├── prod.py              # Production settings (with validation)
└── test.py              # Test settings (SQLite in-memory)
```

### How It Works

1. Set `DJANGO_ENV` environment variable to `dev`, `prod`, or `test`
2. Settings router (`__init__.py`) loads the appropriate module
3. Each environment imports from `base.py` and overrides as needed

**Example:**
```bash
# Development (default)
DJANGO_ENV=dev python manage.py runserver

# Production
DJANGO_ENV=prod python manage.py check --deploy

# Testing (automatic via pytest)
DJANGO_ENV=test pytest
```

---

## Environment Variables

All configuration is done through `.env` file or environment variables.

### Quick Start

```bash
# Copy the example
cp .env.example .env

# Edit with your settings
nano .env
```

### Key Variables

| Variable | Environments | Description |
|----------|--------------|-------------|
| `DJANGO_ENV` | All | Environment: `dev`, `prod`, or `test` |
| `SECRET_KEY` | `prod` | **Required** in production (50+ chars) |
| `DEBUG` | `dev` | Enable debug mode (never in production!) |
| `ALLOWED_HOSTS` | All | Comma-separated hostnames |
| `POSTGRES_HOST` | All | Database host (default: `localhost`) |
| `POSTGRES_DB` | All | Database name |
| `POSTGRES_USER` | All | Database user |
| `POSTGRES_PASSWORD` | All | Database password |
| `POSTGRES_PORT` | All | Database port (default: `5432`) |
| `DJANGO_LOG_LEVEL` | All | Logging level: `DEBUG`, `INFO`, `WARNING` |
| `REDIS_URL` | `prod` | Redis connection string |
| `GUNICORN_WORKERS` | `prod` | Number of Gunicorn workers |
| `GUNICORN_TIMEOUT` | `prod` | Request timeout in seconds |

See [.env.example](../.env.example) for complete list.

---

## Production Settings Example

Production settings are in `core/backend/settings/prod.py` with built-in validation:

```python
# Validates SECRET_KEY is set and strong
SECRET_KEY = env("SECRET_KEY")  # Must be 50+ characters

# Validates ALLOWED_HOSTS is configured
if not ALLOWED_HOSTS:
    sys.exit(1)

# Production security defaults
DEBUG = False
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
```

**No need to copy template files** - just configure via environment variables.

---

## Development Workflow

```bash
# 1. Clone repository
git clone <repo-url>
cd django-v5-starter-template-with-poetry

# 2. Install dependencies
poetry install

# 3. Create .env file
cp .env.example .env

# 4. Edit .env with your settings
nano .env

# 5. Run migrations
make migrate

# 6. Run development server
make runserver
```

---

## Docker Environment Variables

When running in Docker, settings are configured via `docker-compose.yaml`:

```yaml
environment:
  DJANGO_ENV: prod
  POSTGRES_HOST: db
  REDIS_URL: redis://redis:6379/0
env_file:
  - .env
```

**Note:** `POSTGRES_HOST` is set to `db` (Docker service name) automatically.

---

## AWS S3 Configuration for Production Media Files

Django does **not** serve media files (user uploads) in production when `DEBUG=False`. You need a separate solution for production media storage.

### Option 1: Local File Storage (Default)

```bash
# In .env
USE_S3=False  # Default behavior
```

Media files stored at `MEDIA_ROOT` (`/opt/project/media` in Docker).

**⚠️ Note:** You'll need Nginx/Apache to serve these files in production.

### Option 2: AWS S3 Storage (Recommended)

S3 provides scalable, reliable cloud storage for media files.

#### Step 1: Create an S3 Bucket

1. Log in to [AWS Console](https://console.aws.amazon.com/)
2. Navigate to **S3** → **Create bucket**
3. Choose a unique bucket name (e.g., `myproject-media-files`)
4. Select your preferred region (e.g., `us-east-1`)
5. **Uncheck** "Block all public access" (media files need to be publicly accessible)
6. Enable versioning (optional but recommended)
7. Click **Create bucket**

#### Step 2: Configure Bucket CORS

Add CORS configuration to allow your Django app to upload files:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST", "DELETE", "HEAD"],
        "AllowedOrigins": ["https://yourdomain.com", "https://www.yourdomain.com"],
        "ExposeHeaders": ["ETag"],
        "MaxAgeSeconds": 3000
    }
]
```

Apply this in: **S3 Console** → **Your Bucket** → **Permissions** → **CORS configuration**

#### Step 3: Set Bucket Policy

Allow public read access to media files:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::myproject-media-files/media/*"
        }
    ]
}
```

Apply this in: **S3 Console** → **Your Bucket** → **Permissions** → **Bucket Policy**

#### Step 4: Create IAM User with S3 Permissions

1. Navigate to **IAM** → **Users** → **Add user**
2. Choose a username (e.g., `django-s3-user`)
3. Select **Programmatic access**
4. Attach the policy below (or use `AmazonS3FullAccess` for simplicity)
5. Save the **Access Key ID** and **Secret Access Key**

**Recommended IAM Policy** (least privilege):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::myproject-media-files",
                "arn:aws:s3:::myproject-media-files/*"
            ]
        }
    ]
}
```

#### Step 5: Configure Environment Variables

Add the following to your `.env` file:

```bash
# AWS S3 Configuration
USE_S3=True
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_STORAGE_BUCKET_NAME=myproject-media-files
AWS_S3_REGION_NAME=us-east-1
```

The production settings automatically configure S3 when `USE_S3=True`.

#### Step 6: Install Dependencies

The required packages are already in `pyproject.toml`:

```bash
poetry install --with main
# Installs: django-storages[s3] and boto3
```

#### Step 7: Test S3 Integration

```python
# In Django shell
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Test upload
default_storage.save('test.txt', ContentFile(b'Hello S3!'))

# Test URL generation
url = default_storage.url('test.txt')
print(url)  # Should be: https://myproject-media-files.s3.amazonaws.com/media/test.txt

# Test file exists
exists = default_storage.exists('test.txt')
print(exists)  # Should be: True

# Clean up
default_storage.delete('test.txt')
```

### Migrating from Local Storage to S3

If you already have media files stored locally:

```bash
# Option 1: Use AWS CLI to sync files
aws s3 sync /path/to/media/ s3://myproject-media-files/media/ --acl public-read

# Option 2: Use Django management command (create custom command)
python manage.py migrate_media_to_s3
```

### S3 Cost Estimation

AWS S3 pricing (as of 2025, us-east-1):

| Service | Cost |
|---------|------|
| Storage | $0.023 per GB/month |
| PUT requests | $0.005 per 1,000 requests |
| GET requests | $0.0004 per 1,000 requests |
| Data transfer out | $0.09 per GB (first 10 TB/month) |

**Example**: 10 GB storage + 100k uploads + 1M downloads ≈ **$10-15/month**

### Troubleshooting

#### "Access Denied" errors

- Check IAM user has correct permissions
- Verify bucket policy allows public read
- Ensure `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are correct

#### CORS errors in browser

- Check CORS configuration includes your domain
- Verify `AllowedOrigins` matches your `CSRF_TRUSTED_ORIGINS`

#### Files not publicly accessible

- Check bucket policy allows `s3:GetObject` for `media/*`
- Verify bucket policy grants public read access (AWS_DEFAULT_ACL is deprecated)
- Check "Block all public access" is disabled

#### Slow uploads

- Choose S3 region closest to your application server
- Enable S3 Transfer Acceleration (additional cost)
- Use multipart upload for files > 100 MB

### Security Best Practices

1. **Never commit AWS credentials to git**
   - Always use environment variables
   - Add `.env` to `.gitignore`

2. **Rotate credentials regularly**
   - Generate new access keys every 90 days
   - Use AWS Secrets Manager for production

3. **Use separate buckets for dev/staging/prod**
   - Example: `myproject-media-dev`, `myproject-media-prod`

4. **Enable S3 bucket versioning**
   - Protects against accidental deletion
   - Allows file recovery

5. **Set up CloudFront CDN** (optional)
   - Faster delivery via edge locations
   - Reduced S3 costs for frequently accessed files

6. **Monitor S3 usage**
   - Set up AWS billing alerts
   - Use CloudWatch metrics

---

## Security Notes

- The entire `local/` directory is in `.gitignore`
- Only `local/__init__.py` and `local/README.md` are tracked in git
- Never commit files with real secrets or credentials
- Use environment variables for all configuration
- Rotate secrets if accidentally committed

---

## Questions?

See the main [README.md](../README.md) for more information about settings configuration.
