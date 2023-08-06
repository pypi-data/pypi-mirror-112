# hns_logicmonitor_api
Logicmonitor API.

This is mainly built to get data from logicmonitor, especially the optical stats about ONTs. Any other method apart from `get` would need 
to be implemented in the `LMBase` class

## Installation
`pip install hns-logicmonitor-api`

## Usage
```python
from hns_logicmonitor_api import LogicMonitor

with LogicMonitor(
    account_name='account', 
    access_id='test_id', 
    api_key='test_api_key',
    global_timeout=5
) as logic_monitor:
    # Call API here
```
