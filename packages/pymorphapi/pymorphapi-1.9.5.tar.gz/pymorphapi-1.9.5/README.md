# Morpheus Python Module

## Installation

`pip install pymorphapi`

## Usage 

Reference at https://bertramdev.github.io/morpheus-apidoc

```
import pymorphapi

# import and validate/refresh bearer token
bearer_token = pymorphapi.import_token_from_disk(BASE_URI, LOCAL_PATH + TOKEN_FILE, VERIFY_SSL)

# sample get
results = pymorphapi.invoke_api(
    BASE_URI + "/api/roles/?max=1000",
    "Bearer " + bearer_token,
    "get",
    None,
    VERIFY_SSL
)

# sample post
body = {}
body.update({"group": {"name": current_student}})
pymorphapi.invoke_api(
    BASE_URI + "/api/accounts/" + str(new_tenant_id) + "/groups/",
    "Bearer " + bearer_token,
    "post",
    body,
    VERIFY_SSL
)

```