import binance

def I__GET_SYSTEM_STATUS(client):
    try:
        ret = client.get_system_status()
    except:
        ret = 2
    
    return ret['status']

