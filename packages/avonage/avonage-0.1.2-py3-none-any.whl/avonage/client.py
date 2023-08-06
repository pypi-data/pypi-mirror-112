import asyncio
import base64
import copy
import logging
import os
import re
from platform import python_version

import aiohttp as aiohttp

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


async def send_sms(from_num, to_num, text, loop, key=None, secret=None):
    client = VonageAsync(key=key, secret=secret)
    response_data = await client.send_message(
        {
            'from': from_num,
            'to': to_num,
            'text': text,
            'type': 'unicode'
        },
        loop=loop
    )
    if response_data["messages"][0]["status"] == "0":
        logger.info("Message sent successfully.")
        return True
    else:
        error = response_data['messages'][0]['error-text']
        logger.error(
            f"SMS message failed with error: {error}")
        return False


class VonageError(Exception):
    pass


class VonageAsync:
    __version__ = "2.4.0"

    def __init__(self, key=None, secret=None, signature_secret=None):
        self.api_key = key or os.environ.get("VONAGE_KEY", None)
        self.api_secret = secret or os.environ.get("VONAGE_SECRET", None)
        self.signature_secret = signature_secret or os.environ.get(
            "VONAGE_SIGNATURE_SECRET", None
        )
        self.__host = "rest.nexmo.com"
        self.__api_host = "api.nexmo.com"
        user_agent = "vonage-python/{version} python/{python_version}".format(
            version=self.__version__, python_version=python_version()
        )
        self.headers = {"User-Agent": user_agent}

    def host(self, value=None):
        if value is None:
            return self.__host
        elif not re.match(self.__host_pattern, value):
            raise Exception("Error: Invalid format for host")
        else:
            self.__host = value

    async def post(
            self,
            host,
            request_uri,
            params,
            session,
            supports_signature_auth=False,
            header_auth=False,
    ):
        uri = "https://{host}{request_uri}".format(host=host, request_uri=request_uri)
        headers = self.headers
        if supports_signature_auth and self.signature_secret:
            params["api_key"] = self.api_key
            params["sig"] = self.signature(params)
        elif header_auth:
            h = base64.b64encode(
                (
                    "{api_key}:{api_secret}".format(
                        api_key=self.api_key, api_secret=self.api_secret
                    ).encode("utf-8")
                )
            ).decode("ascii")
            headers = dict(headers or {}, Authorization="Basic {hash}".format(hash=h))
        else:
            params = dict(params, api_key=self.api_key, api_secret=self.api_secret)
        # Prepare for logging
        _params = copy.copy(params)
        _params['api_key'] = '****'
        _params['api_secret'] = '****'
        logger.debug("POST to %r with params %r, headers %r", uri, _params, headers)

        async with session.post(uri, headers=headers, json=params) as response:
            status = response.status
            vonage_response = await response.json()
            if status >= 400:
                raise VonageError('Error duriong Vonage API call.')
            logger.info(f'Requested Vonage API call with status ({status})')
        return vonage_response

    async def send_message(self, params, loop, future=None):
        async with aiohttp.ClientSession(loop=loop) as session:
            response = await self.post(host=self.host(),
                                       request_uri="/sms/json",
                                       params=params,
                                       session=session,
                                       supports_signature_auth=True)
            if not future:
                return response
        future.set_result(response)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Just to try / test two options
    run_with_future = True
    # Option 1: With future
    if run_with_future:
        future = asyncio.Future()
        params = {
            'from': os.getenv('VONAGE_VIRTUAL_NUM'),
            'to': os.getenv('VONAGE_RECEIVER_NUM'),
            'text': 'Hi there!',
            'type': 'unicode'
        }
        asyncio.ensure_future(VonageAsync().send_message(params, loop, future))
        loop.run_until_complete(future)
        logger.debug(future.result())
    # Option 2: With awaitable
    else:
        loop.run_until_complete(send_sms(key=os.environ.get("VONAGE_KEY", None),
                                         secret=os.environ.get("VONAGE_SIGNATURE_SECRET", None),
                                         from_num=os.getenv('VONAGE_VIRTUAL_NUM'),
                                         to_num=os.getenv('VONAGE_RECEIVER_NUM'),
                                         sms_text='Hi there!',
                                         loop=loop))
    loop.close()
