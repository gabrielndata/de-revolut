import json
from app import API_PREFIX


def test_nestify_resource_post_ok(client, flat_data, folded_data, auth_headers):

    response = client.post(f'{API_PREFIX}/nestify', json=flat_data, query_string={
        'group_by': 'currency, country, city'}, headers=auth_headers)
    assert json.loads(response.data) == folded_data
    assert response.status == '200 OK'


def test_nestify_resource_post_not_found(client, flat_data, auth_headers):
    response = client.post(f'{API_PREFIX}/nestify', json=flat_data, query_string={
        'group_by': 'hello'}, headers=auth_headers)
    assert json.loads(response.data)['root'] == flat_data
    assert response.status == '200 OK'


def test_nestify_resource_post_bad_request(client, flat_data, auth_headers):
    response = client.post(f'{API_PREFIX}/nestify', data='bad_json', headers=auth_headers)
    assert response.status == '400 BAD REQUEST'
    response = client.post(f'{API_PREFIX}/nestify', json='bad_json', headers=auth_headers)
    assert response.status == '400 BAD REQUEST'


def test_nestify_resource_post_unauthorized(client, flat_data):
    response = client.post(f'{API_PREFIX}/nestify')
    assert response.status == '401 UNAUTHORIZED'
