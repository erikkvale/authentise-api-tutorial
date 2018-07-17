from pprint import pprint
import requests
import time
from config.user import USERNAME, PASSWORD


def main():
    session = authentise_login(
        username=USERNAME,
        password=PASSWORD
    )

    # model payload/upload on current session
    payload = {
        'auto-align': False,
        'name': 'demo model'
    }
    response = session.post(
        url='https://models.authentise.com/model',
        json=payload
    )
    if _check_response(response):
        # Headers in video seem to be outdated ways of gathering urls,
        # adjusted to get from json() response and 'resources' sub dict
        unpacked_response = response.json()['resources'][0]
        model_url = unpacked_response['uri']
        upload_url = unpacked_response['upload-location']

        with open('./models/vertebra.stl', 'rb') as f:
            response = session.put(
                url=upload_url,
                data=f.read(),
                headers={
                    'Content-Type': 'application/octet-stream'
                }
            )
            if _check_response(response):
                _wait_on_status(
                    session,
                    model_url,
                    ('error', 'processed')
                )


def _wait_on_status(session, url, statuses):
    data = {'status': ''}
    while data['status'] not in statuses:
        response = session.get(url)
        if _check_response(response):
            data = response.json()
            pprint(data)
            print('-' * 20)
            time.sleep(0.5)
    return data


def authentise_login(username, password, url='https://users.authentise.com/sessions/'):
    """
    Returns a requests.Session() object if
    the supplied username and password were
    successfully authenticated
    """
    session = requests.Session()
    payload = {
        'username': username,
        'password': password,
    }
    response = session.post(url, json=payload)
    if _check_response(response):
        return session


def _check_response(response):
    if response.ok:
        return True
    else:
        raise requests.HTTPError(
            "Check the response, response code: {}".format(
                response.status_code
            )
        )

if __name__=='__main__':
    main()
