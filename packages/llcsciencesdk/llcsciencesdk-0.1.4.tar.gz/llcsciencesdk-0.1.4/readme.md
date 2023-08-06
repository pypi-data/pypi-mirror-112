# LLC Science SDK

> A simple way to fetch scientific data. 

## Installation

```sh
pip install llcsciencesdk
```

## Usage

#### Getting data from new API version

```python
from llcsciencesdk.llc_api import ScienceSdk

llc_api = ScienceSdk()
llc_api.login("username", "password")
model_input = llc_api.get_model_inputs(1)
```

#### Connecting to staging is also possible

```python
from llcsciencesdk.llc_api import ScienceSdk

llc_api = ScienceSdk(environment="staging")
llc_api.login("username", "password")
model_input = llc_api.get_model_inputs(1)
```

#### Getting data from old API version


```python
from llcsciencesdk.llc_api import ScienceSdk

llc_api = ScienceSdk(environment="staging")
llc_api.login("username", "password")
model_input = llc_api.get_old_model_inputs([43])
```
