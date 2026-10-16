import httpx
from app.main import app
from app.product_client import get_product_fetcher

def fake_fetch_product(product_id: int) -> dict:
    return {"id": product_id, "name": "Laptop", "price": 899}

def provide_fake_product():
    return fake_fetch_product

def test_remote_product_success(client):
    app.dependency_overrides[get_product_fetcher] = provide_fake_product
    try:
        response = client.get("/api/products/1")
        assert response.status_code == 200
        assert response.json()["name"] == "Laptop"
    finally:
        app.dependency_overrides.pop(get_product_fetcher, None)

def fake_product_missing(product_id: int):
    request = httpx.Request(
        "GET", f"http://example.test/products/{product_id}"
    )
    response = httpx.Response(404, request=request)
    raise httpx.HTTPStatusError(
        "Not found", request=request, response=response
    ) 

def provide_missing_product():
    return fake_product_missing

def test_remote_product_missing(client):
    app.dependency_overrides[get_product_fetcher] = provide_missing_product
    try:
        response = client.get("/api/products/99")
        assert response.status_code == 404
    finally:
        app.dependency_overrides.pop(get_product_fetcher, None)

def fake_service_unavailable(product_id: int):
    request = httpx.Request(
        "GET", f"http://example.test/products/{product_id}"
    )
    raise httpx.ConnectError("Connection refused", request=request)

def provide_unavailable_product():
    return fake_service_unavailable

def test_remote_service_unavailable(client):
    app.dependency_overrides[get_product_fetcher] = provide_unavailable_product
    try:
        response = client.get("/api/products/1")
        assert response.status_code == 503
    finally:
         app.dependency_overrides.pop(get_product_fetcher, None)