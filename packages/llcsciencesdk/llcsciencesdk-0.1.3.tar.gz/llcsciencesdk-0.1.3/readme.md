# LLC Science SDK

> A simple way to fetch scientific data. 

## Installation

```sh
pip install llcsciencesdk
```

## Usage

```python
from llcsciencesdk.llc_api import ScienceSdk

llc_api = ScienceSdk()
llc_api.login("username", "password")
model_input = llc_api.get_model_inputs(1)
```

#### Connect to staging is also possible

```python
from llcsciencesdk.llc_api import ScienceSdk

llc_api = ScienceSdk(environment="staging")
llc_api.login("username", "password")
model_input = llc_api.get_model_inputs(1)
```