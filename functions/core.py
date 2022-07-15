from urllib import response
from .datastrg.apikeys import Keys
import json, time, hashlib, hmac
from urllib.parse import urlencode
import asyncio
import httpx

async def get_signed_params_headers(params):
    async with httpx.AsyncClient() as client:
        servertime = await client.get("https://api.binance.com/api/v1/time")

    servertimeobject = json.loads(servertime.text)
    servertimeint = servertimeobject['serverTime']
    params["timestamp"] = servertimeint

    enc_params = urlencode(params)
    hashedsig = hmac.new(Keys.private.encode(), enc_params.encode(), hashlib.sha256).hexdigest()

    params["signature"] = hashedsig

    headers = {"X-MBX-APIKEY" : Keys.public}

    return params, headers

async def open_spot(symbol, qnt):
    
    #spot params
    async with httpx.AsyncClient() as client:
        price = await client.get('https://api.binance.com/api/v3/ticker/bookTicker', params={'symbol':symbol})
    price = price.json()['askPrice']

    sp = {
        'symbol': symbol,
        'side': 'BUY',
        'type': 'LIMIT',
        'quantity': float(qnt),
        'price': round(float(price)*1.001, 2),
        'timeInForce': 'GTC',
    }

    params, headers = await get_signed_params_headers(sp)

    #print(requests.post('https://api.binance.com/api/v3/order/test', params=params, headers=headers))
    async with httpx.AsyncClient() as client:
        print(await client.post('https://api.binance.com/api/v3/order', params=params, headers=headers))


async def open_futures(symbol, qnt):
    #futures params
    async with httpx.AsyncClient() as client:
        price = await client.get('https://fapi.binance.com/fapi/v1/depth', params={'symbol':symbol, 'limit':5})
    price = price.json()['bids'][0][0]

    fp = {
        'symbol': symbol,
        'side': 'SELL',
        'type': 'LIMIT',
        'quantity': float(qnt),
        'price': float(price),
        'timeInForce': 'GTC',
    }

    params, headers = await get_signed_params_headers(fp)

    #print(requests.post('https://testnet.binancefuture.com/fapi/v1/order', params=params, headers=headers))
    async with httpx.AsyncClient() as client:
        print(await client.post('https://fapi.binance.com/fapi/v1/order', params=params, headers=headers))