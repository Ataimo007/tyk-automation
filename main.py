import argparse
from api.oas_bulk_jwt_manager import create_apis, create_apis_with_product_payload_render, delete_apis

def main():
    parser = argparse.ArgumentParser(
        description="Tyk Automation Suite - OAS API Manager"
    )

    parser.add_argument("--api-name", required=True)
    parser.add_argument("--number", type=int, default=1)
    parser.add_argument("--jwks-uri")
    parser.add_argument("--delete", action="store_true")

    # product render args
    parser.add_argument("--provider-id")
    parser.add_argument("--templates")
    parser.add_argument("--product-payload", action="store_true")

    args = parser.parse_args()

    if args.delete:
        delete_apis(args.api_name)
        return

    if args.product_payload:

        if not args.provider_id or not args.templates:
            print("❌ --provider-id and --template-id are required for product payload")
            return

        create_apis_with_product_payload_render(
            api_name=args.api_name,
            number=args.number,
            jwks_uri=args.jwks_uri,
            provider_id=args.provider_id,
            templates=args.templates
        )
        return

    if not args.jwks_uri:
        print("❌ --jwks-uri required when creating APIs")
        return

    create_apis(
        api_name=args.api_name,
        number=args.number,
        jwks_uri=args.jwks_uri
    )

if __name__ == "__main__":
    main()
