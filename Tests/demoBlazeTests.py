import requests
import base64

USERNAME = "ViaUserTest"
PASSWORD = "Aa123456"
DEMO_BLAZE_BASE_URL = "https://api.demoblaze.com"


def test_validate_nexus6_product():
    verify_product(verify_items_count_and_get_product_id(get_user_cookie_via_login()))


def get_user_cookie_via_login():
    user_login_details = {"username": USERNAME, "password": get_password_base64().decode()}
    login_response = requests.post(f"{DEMO_BLAZE_BASE_URL}/login", json=user_login_details)
    assert login_response.status_code == 200
    return get_user_cookie(login_response)


def verify_items_count_and_get_product_id(user_cookie):
    user_credentials_data = {"cookie": user_cookie, "flag": True}
    view_cart_response = requests.post(f"{DEMO_BLAZE_BASE_URL}/viewcart", json=user_credentials_data)
    assert view_cart_response.status_code == 200
    verify_items_count(view_cart_response)
    verify_product_id(view_cart_response)
    return view_cart_response.json()["Items"][0]["prod_id"]


def verify_product(product_id):
    product_data = {"id": product_id}
    view_response = requests.post(f"{DEMO_BLAZE_BASE_URL}/view", json=product_data)
    assert view_response.status_code == 200
    verify_product_title(view_response)
    verify_product_price(view_response)


def get_password_base64():
    password = PASSWORD
    return base64.b64encode(password.encode('ascii'))


def get_user_cookie(login_response):
    return login_response.content.decode().replace('\"\n', "").split(": ")[1]


def verify_items_count(view_cart_response):
    assert len(view_cart_response.json()) == 1


def verify_product_id(view_cart_response):
    assert view_cart_response.json()["Items"][0]["prod_id"] == 3


def verify_product_title(view_response):
    assert view_response.json()["title"] == "Nexus 6"


def verify_product_price(view_response):
    assert view_response.json()["price"] == 650

