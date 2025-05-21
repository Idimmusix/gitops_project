import random
import string

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    # --- Debugging ---
    print(f"Login API Status Code: {r.status_code}")
    print(f"Login Data: {login_data}")
    try:
        print(f"Login API Response JSON: {r.json()}")
    except Exception as e:
        print(f"Login API Response Text (not JSON or error parsing): {r.text}")
        print(f"JSONDecodeError: {e}")
    # --- End Debugging ---

    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
