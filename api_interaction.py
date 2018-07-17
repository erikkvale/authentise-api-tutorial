from pprint import pprint
import requests
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
        model = response.headers['Location']
        upload_url = response.headers['X-Upload-Location']
        with open('./models/RhinoBone.stl', 'rb') as f:
            response = session.put(
                url=upload_url,
                data=f.read(),
                headers={
                    'Content-Type': 'application/octet-stream'
                }
            )
            assert _check_response(response)

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
