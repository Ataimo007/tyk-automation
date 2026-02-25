import requests
from config.settings import DASHBOARD_URL, API_KEY, ORG_ID
import json

headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY
}

import base64

def generate_oas_api(api_name, index, jwks_uri):

    api_full_name = f"{api_name}-{index}"
    listen_path = f"/{api_full_name}/"

    return {
        "info": {
            "title": api_full_name,
            "version": "1.0.0"
        },
        "openapi": "3.0.3",
        "servers": [
            {
                "url": listen_path
            }
        ],
        "security": [
            {
                "jwtAuth": []
            }
        ],
        "paths": {},

        "components": {
            "securitySchemes": {
                "jwtAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        },

        "x-tyk-api-gateway": {
            "info": {
                "id": "",
                "orgId": ORG_ID,
                "name": api_full_name,
                "state": {
                    "active": True,
                    "internal": False
                }
            },

            "upstream": {
                "proxy": {
                    "enabled": False,
                    "url": ""
                },
                "url": "http://httpbin.org/"
            },

            "server": {
                "authentication": {
                    "enabled": True,
                    "securitySchemes": {
                        "jwtAuth": {
                            "header": {
                                "enabled": True,
                                "name": "Authorization"
                            },
                            "identityBaseField": "sub",
                            "jtiValidation": {
                                "enabled": False
                            },
                            "policyFieldName": "pol",
                            "enabled": True,
                            "defaultPolicies": [],
                            "basePolicyClaims": ["pol"],
                            "subjectClaims": ["sub"],
                            "signingMethod": "rsa",

                            # 👇 Dynamic Base64 encoding of JWKS URI
                            "source": base64.b64encode(jwks_uri.encode()).decode()
                        }
                    }
                },

                "listenPath": {
                    "value": listen_path,
                    "strip": True
                }
            },

            "middleware": {
                "global": {
                    "contextVariables": {
                        "enabled": True
                    },
                    "trafficLogs": {
                        "enabled": True
                    }
                }
            }
        }
    }

def create_apis_with_product_payload_render(api_name, number, jwks_uri, provider_id, templates):

    api_details = []

    print(f"\n🚀 Creating {number} OAS JWT APIs...\n")

    for i in range(1, number + 1):

        api_definition = generate_oas_api(api_name, i, jwks_uri)

        response = requests.post(
            f"{DASHBOARD_URL}/api/apis/oas",
            headers=headers,
            json=api_definition
        )

        if response.status_code == 200:

            resp = response.json()
            api_id = resp.get("ID")

            print(f"✅ Created: {api_name}-{i} (ID: {api_id})")

            # 👇 gather details inside loop
            gather_api_details(api_details, api_id, api_definition["info"]["title"])

        else:
            print(f"❌ Failed: {api_name}-{i}")
            print(response.status_code, response.text)

    # 👇 compile product after loop
    product = compile_product_payload(api_details, api_name, provider_id, templates)

    print("\n🧾 Compiled product payload (dry run):\n")
    print(json.dumps(product, indent=4))

def create_apis(api_name, number, jwks_uri):

    print(f"\n🚀 Creating {number} OAS JWT APIs...\n")

    for i in range(1, number + 1):

        api_definition = generate_oas_api(api_name, i, jwks_uri)

        response = requests.post(
            f"{DASHBOARD_URL}/api/apis/oas",
            headers=headers,
            json=api_definition
        )

        if response.status_code == 200:
            print(f"✅ Created: {api_name}-{i}")
        else:
            print(f"❌ Failed: {api_name}-{i}")
            print(response.status_code, response.text)

def gather_api_details(api_details, api_id, api_name):

    api_details.append({
        "APIID": api_id,
        "Description": api_name,
        "OASUrl": "https://httpbin.org/spec.json"
    })

def compile_product_payload(api_details, api_name, provider_id, templates):

    return {
        "APIDetails": api_details,
        "Catalogues": [1],
        "Content": api_name,
        "DCREnabled": True,
        "Description": api_name,
        "DisplayName": api_name,
        "Feature": True,
        "IsDocumentationOnly": False,
        "Name": api_name,
        "ProviderID": provider_id,
        "Scopes": "payments, clients",
        "Tags": [],
        "Templates": [templates]
    }

def delete_apis(api_name):

    print("\n🧹 Deleting APIs (with pagination)...\n")

    page = 1
    total_deleted = 0

    while True:

        response = requests.get(
            f"{DASHBOARD_URL}/api/apis?page={page}",
            headers=headers
        )

        if response.status_code != 200:
            print(f"❌ Failed to fetch APIs on page {page}")
            print(response.text)
            break

        data = response.json()

        apis = data.get("apis", [])
        pages = data.get("pages", 1)

        print(f"📄 Processing page {page} of {pages}")

        for api_entry in apis:

            api_def = api_entry.get("api_definition", {})

            name = api_def.get("name", "")
            api_id = api_def.get("id")

            if name.startswith(api_name):

                delete_response = requests.delete(
                    f"{DASHBOARD_URL}/api/apis/{api_id}",
                    headers=headers
                )

                if delete_response.status_code == 200:
                    print(f"🗑 Deleted: {name}")
                    total_deleted += 1
                else:
                    print(f"❌ Failed to delete: {name}")
                    print(delete_response.text)

        # Stop if we reached the last page
        if page >= pages:
            break

        page += 1

    print(f"\n✅ Deletion complete. Total deleted: {total_deleted}")