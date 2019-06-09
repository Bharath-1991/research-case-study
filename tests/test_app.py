
import requests
import json

url = "http://localhost:5000/customers"

test_data = { 
                "name":"test-name",
                "address":"London",
	            "postcode":"ILLFORRDD"
            }

'''For each test case i am creating new values and deleting those values at the end of test case '''

def test_put_customers():
    headers={"Content-Type":"application/json"}
    response = requests.put(url,data=json.dumps(test_data), headers=headers)
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert 'Values updated successfully' == response.get('message')
    assert response.get('updated_values')[0].get('name') == 'test-name'

    response = requests.put(url,data=json.dumps({"name":"bharath"}), headers=headers, params={'expire_in':60})
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert 'Values updated successfully' == response.get('message')
    assert int(response.get('updated_values')[0].get('expire_in')) == 60
    assert response.get('updated_values')[0].get('name') == 'bharath'
    response = requests.delete(url)


def test_get_customers():
    requests.put(url,data=json.dumps(test_data), headers={"Content-Type":"application/json"})
    response = requests.get(url)
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert response.get('customer_details') == test_data

    url_with_specific_key = url + '/name'
    response = requests.get(url_with_specific_key)
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert response.get('customer_details').get('name') == 'test-name'

    response = requests.get(url, params={"filter":"na$e"})
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert response.get('customer_details').get('name') == 'test-name'

    response = requests.delete(url)


def test_check_value_exists():
    requests.put(url,data=json.dumps(test_data), headers={"Content-Type":"application/json"})
    
    url_with_specific_key = url + '/name'
    response = requests.head(url_with_specific_key)
    assert response.status_code == 200

    url_with_specific_key = url + '/name123'
    response = requests.head(url_with_specific_key)
    assert response.status_code == 404

    response = requests.delete(url)

def test_delete_customer_details():
    requests.put(url,data=json.dumps(test_data), headers={"Content-Type":"application/json"})
    url_with_specific_key = url + '/name'
    response = requests.delete(url_with_specific_key)
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert 'Values updated successfully' == response.get('message')
    assert response.get('updated_values')[0].get('name') is None

    response = requests.delete(url)
    assert response is not None
    assert response.status_code == 200
    response = response.json()
    assert 'Successfully Deleted' == response.get('message')







