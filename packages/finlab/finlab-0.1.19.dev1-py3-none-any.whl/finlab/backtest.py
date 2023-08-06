from . import get_token
import requests
from finlab.utils import auth_permission, raise_permission_error


def get_simulator_on_cloud():
    api_token = get_token()

    request_args = {
        'api_token': api_token,
        'bucket_name':'finlab_tw_stock_item',
        'blob_name': 'simulator/backtest_encrypted.pye',
    }

    url = 'https://asia-east2-fdata-299302.cloudfunctions.net/auth_generate_data_url'
    auth_url = requests.get(url, request_args)
    getUrl(auth_url.text)

try:
    from . import backtest_encrypted
    sim = backtest_encrypted.sim
except:
    try:
        import sourcedefender
        from sourcedefender.tools import getUrl
        get_simulator_on_cloud()
        import backtest_encrypted
        sim = backtest_encrypted.sim
    except:
        sim = raise_permission_error

