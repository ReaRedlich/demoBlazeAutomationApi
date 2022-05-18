import requests
import base64

USERNAME = "ViaUserTest"
PASSWORD = "Aa123456"
EXPECTED_PRODUCT_TITLE = "Nexus 6"
DEMO_BLAZE_BASE_URL = "https://api.demoblaze.com"

INDEX = 0
EXPECTED_ITEMS_COUNT = 1
EXPECTED_PRODUCT_NEXUS6_ID = 3
EXPECTED_PRODUCT_NEXUS6_PRICE = 650
EXPECTED_STATUS_CODE_OK = 200


def test_validate_for_nexus6_product():
    verify_product(verify_items_count_and_get_product_id(get_user_cookie_via_login()))


def get_user_cookie_via_login():
    user_login_details = {"username": USERNAME, "password": get_password_base64().decode()}
    login_response = requests.post(f"{DEMO_BLAZE_BASE_URL}/login", json=user_login_details)
    assert login_response.status_code == EXPECTED_STATUS_CODE_OK

    return get_user_cookie(login_response)


def verify_items_count_and_get_product_id(user_cookie):
    user_credentials_data = {"cookie": user_cookie, "flag": True}
    view_cart_response = requests.post(f"{DEMO_BLAZE_BASE_URL}/viewcart", json=user_credentials_data)
    assert view_cart_response.status_code == EXPECTED_STATUS_CODE_OK

    view_cart_response_json_body = view_cart_response.json()
    verify_items_count(view_cart_response_json_body, EXPECTED_ITEMS_COUNT)
    verify_product_id_after_view_cart_api(view_cart_response_json_body, INDEX, EXPECTED_PRODUCT_NEXUS6_ID)

    return view_cart_response_json_body["Items"][INDEX]["prod_id"]


def verify_product(product_id):
    product_data = {"id": product_id}
    view_response = requests.post(f"{DEMO_BLAZE_BASE_URL}/view", json=product_data)
    assert view_response.status_code == EXPECTED_STATUS_CODE_OK

    view_response_json_body = view_response.json()
    verify_product_id_after_view_api(view_response_json_body, product_id)
    verify_product_title(view_response_json_body, EXPECTED_PRODUCT_TITLE)
    verify_product_price(view_response_json_body, EXPECTED_PRODUCT_NEXUS6_PRICE)


def get_password_base64():
    password = PASSWORD
    return base64.b64encode(password.encode('ascii'))


def get_user_cookie(login_response):
    return login_response.content.decode().replace('\"\n', "").split(": ")[1]


def verify_items_count(view_cart_response_json_body, expected_count):
    assert len(view_cart_response_json_body) == expected_count


def verify_product_id_after_view_cart_api(view_cart_response_json_body, item_index, expected_product_id):
    assert view_cart_response_json_body["Items"][item_index]["prod_id"] == expected_product_id


def verify_product_id_after_view_api(view_response_json_body, expected_product_id):
    assert view_response_json_body["id"] == expected_product_id


def verify_product_title(view_response_json_body, expected_title):
    assert view_response_json_body["title"] == expected_title


def verify_product_price(view_response_json_body, expected_price):
    assert view_response_json_body["price"] == expected_price

