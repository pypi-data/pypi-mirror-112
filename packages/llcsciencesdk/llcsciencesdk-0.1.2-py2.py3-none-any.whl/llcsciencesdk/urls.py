from collections import namedtuple

ApiUrls = namedtuple("Urls", "AUTH_URL GET_MODEL_INPUT_URL")


def make_urls(environment):
    BASE_API_URL = (
        "https://internal-landlifecompany.appspot.com/"
    )

    if environment == "staging":
        BASE_API_URL = (
            "https://staging-science-admin-dot-internal-landlifecompany.ue.r.appspot.com"
        )

    return ApiUrls(
        AUTH_URL=f'{BASE_API_URL}/api/v1/token/',
        GET_MODEL_INPUT_URL=f"{BASE_API_URL}/sciencemodel/fasttrackinput/planting_design_config/"
    )
