This application originally contained several issues related to security, reliability, and maintainability. The following improvements were made while keeping the solution simple and easy to run.

## What fixed

### 1. Environment Configuration

* Replaced hardcoded values with environment variables:

  * `FILE_SECRET` → used for authentication
  * `APP_PORT` → configurable port with default fallback

* Prevents crashes and improves flexibility across environments

### 2. Application Stability

* Added fallbacks to avoid runtime issues
* Handled missing headers and invalid requests with an error message
* Added proper HTTP status codes and JSON values

### 3. File Handling Safety

* Prevented crashes when files don’t exist
* Ensured image directory is created automatically
* Switched to safer file path handling using `pathlib`

### 4. Security Improvements

* Removed hardcoded secrets from source code
* Added validation for incoming requests

### 5. Better API Behavior

* Consistent JSON responses for errors and success
* Proper HTTP status codes:

  * `200` → success
  * `201` → created
  * `400` → bad request
  * `403` → unauthorized
  * `404` → not found



# Running the Application

## Using Docker Compose

```bash
docker-compose up --build
```

Application will be available at:

```
http://localhost:5000
```


## Environment Variables (Optional)

| Variable    | Description               | Default    |
| -- | - | - |
| APP_PORT    | Application port          | 5000       |
| FILE_SECRET | Secret key for API access | h20tavyWvchAlZko21t0X0lH93VJCQBn |



# APIs

All apis require a header:

```
X-Image-Secret: <your-secret>
```
## Health Check

```bash
curl http://localhost:5000/
```

### Response

```json
{
  "status": "running",
  "message": "Use /image/<file_name>"
}
```



## Upload an Image

```bash
curl -X POST http://localhost:5000/image/test \
  -H "X-Image-Secret: dev-secret" \
  --data-binary @sample.png
```

### Response

```json
{
  "status": "saved"
}
```

## Fetch an Image

```bash
curl http://localhost:5000/image/test \
  -H "X-Image-Secret: dev-secret" \
  --output downloaded.png
```

## Error Scenarios

### Missing Secret

```bash
curl http://localhost:5000/image/test
```

Response:

```
403 Forbidden
```



### File Not Found

```bash
curl http://localhost:5000/image/unknown \
  -H "X-Image-Secret: dev-secret"
```

Response:

```
404 Not Found
```



### Empty Upload

```bash
curl -X POST http://localhost:5000/image/test \
  -H "X-Image-Secret: dev-secret"
```

Response:

```json
{
  "error": "No data provided"
}
```
