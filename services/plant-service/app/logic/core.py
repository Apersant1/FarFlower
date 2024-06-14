import jwt
import datetime



# Example usage:
# Define the claims ( payload )
payload = {
    "sub": "user_id",  # subject (user ID)
    "aud": ["fastapi-users:auth"],  # audience (authorized parties)
    "is_superuser": False,  # custom claim (is superuser?)
    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # expiration time (30 minutes)
}

# Define the secret key
secret_key = "SECRET"

# Generate the token
encoded = jwt.encode(payload, "secret", algorithm="HS256")

print(jwt.decode(encoded, "secret", audience="fastapi-users:auth",algorithms=["HS256"]))