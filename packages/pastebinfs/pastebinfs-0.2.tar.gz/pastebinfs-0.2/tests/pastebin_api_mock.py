import requests_mock
import pastebinfs.sync
import requests
from urllib.parse import parse_qs
import base64

def poste_endpoint_list():
    return """
<paste>
    <paste_key>0b42rwhf</paste_key>
    <paste_date>1297953260</paste_date>
    <paste_title>test.txt</paste_title>
    <paste_size>15</paste_size>
    <paste_expire_date>1297956860</paste_expire_date>
    <paste_private>0</paste_private>
    <paste_format_long>JavaScript</paste_format_long>
    <paste_format_short>javascript</paste_format_short>
    <paste_url>https://pastebin.com/0b42rwhf</paste_url>
    <paste_hits>15</paste_hits>
</paste>
"""


def poste_endpoint(request: requests.Request, context):
    context.status_code = 200
  
    post_body = parse_qs(request.text)
    if post_body['api_option'][0] == 'list':
        return poste_endpoint_list() # Example response

    elif post_body['api_option'][0] == 'paste':
        assert post_body['api_paste_private'][0] == '1' # unlisted
        assert post_body['api_paste_name'][0] == 'test.txt'
        assert post_body['api_user_key'][0] == '837AD232A4F231AFF'        
        return "https://pastebin.com/421dfaw3" # new oaste id

    elif post_body['api_option'][0] == 'delete':
        assert post_body['api_paste_key'][0] == "0b42rwhf", "Deleted wrong paste"
        return "Paste Removed" 

    raise Exception(f"invalid operation {post_body['api_option']}")

def raw_endpoint(request: requests.Request, context):
    context.status_code = 200
    return base64.b64encode("this is the content of test.txt".encode()).decode()

def setup_fake_pastebin_api(requests_mock: requests_mock.Mocker):
    requests_mock.post('https://pastebin.com/api/api_login.php', text='837AD232A4F231AFF')
    requests_mock.register_uri('POST', 'https://pastebin.com/api/api_post.php', text=poste_endpoint, status_code=200)
    requests_mock.register_uri('POST', 'https://pastebin.com/api/api_raw.php', text=raw_endpoint, status_code=200) # todo check if api_option is 'show_paste'

