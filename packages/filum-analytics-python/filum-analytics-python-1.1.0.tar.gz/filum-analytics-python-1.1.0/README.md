# filum-python-sdk
Filum Python SDK to send events to Filum Event API

## Installation
1. Clone this repository, get into its root folder that contains `setup.py`: 
```buildoutcfg
  pip install .
```

2. Use it in your code:
```buildoutcfg
    from filum_analytics.client import Client
    _client = Client(write_key=<YOUR WRITE KEY>,
                     host="https://event.filum.ai")
    analytics_python = _client
    import uuid

    analytics_python.identify(user_id=str(uuid.uuid4()), event_params={
        "username": "Elon Musketeer",
        "email": "elon@tesla.com"
    })
    
    # track call for Server source like Python or NodeJS must include anonymousID or userID
    analytics_python.track(anonymous_id=str(uuid.uuid4()), event_name="Testing event sent", event_params={
        "attribute": "Sample attribute",
        "integer": 5,
        "float": 5.5
    })
```

## License
[Based on Segment Python SDK](https://github.com/segmentio/analytics-python)
```
WWWWWW||WWWWWW
 W W W||W W W
      ||
    ( OO )__________
     /  |           \
    /o o|    MIT     \
    \___/||_||__||_|| *
         || ||  || ||
        _||_|| _||_||
       (__|__|(__|__|
```

(The MIT License)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

