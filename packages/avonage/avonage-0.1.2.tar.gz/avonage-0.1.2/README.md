# Avonage

### Description

Avonage is an implementation of asynchronous client for Vonage / Nexmo. The package offers async client as a class for inheritance and extension and **send_sms** method, which abstracts Vonage / Nexmo API call to send a SMS.


### Installation

```bash
pip install avonage
```

### Usage
Before using the package, please consider to getting Vonage / Nexmo API key and secret.
You can specify Vonage credentials as environment variables or pass directly to function.
Package can pick next environment variables:
```bash
    ============= Most often used ============
    VONAGE_KEY
    VONAGE_SECRET
    ==========================================
    VONAGE_SIGNATURE_SECRET
```



Option 1: With future
```python
import os
import asyncio

from avonage.client import VonageAsync



loop = asyncio.get_event_loop()
future = asyncio.Future()
params = {
    'from': os.getenv('VONAGE_VIRTUAL_NUM'),
    'to': os.getenv('VONAGE_RECEIVER_NUM'),
    'text': 'Hi there!',
    'type': 'unicode'
}
asyncio.ensure_future(VonageAsync().send_message(params, loop, future))
loop.run_until_complete(future)

```

Option 2: With awaitable
```python
import os
import asyncio

from avonage.client import send_sms

loop = asyncio.get_event_loop()
loop.run_until_complete(send_sms(key=os.environ.get("VONAGE_KEY", None),
                                 secret=os.environ.get("VONAGE_SECRET", None),
                                 from_num=os.getenv('VONAGE_VIRTUAL_NUM'),
                                 to_num=os.getenv('VONAGE_RECEIVER_NUM'),
                                 text='Hi there!',
                                 loop=loop))
```
