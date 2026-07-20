import argparse
from pathlib import Path

try:
    from .manager import AssetManager
except ImportError:  # pragma: no cover - supports running this file directly
    from manager import AssetManager


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Asset Pro CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List all assets")

    add_parser = subparsers.add_parser("add", help="Add a new asset")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--category", required=True)
    add_parser.add_argument("--value", type=float, required=True)
    add_parser.add_argument("--status", default="active")

    update_parser = subparsers.add_parser("update", help="Update an asset")
    update_parser.add_argument("asset_id")
    update_parser.add_argument("--name")
    update_parser.add_argument("--category")
    update_parser.add_argument("--value", type=float)
    update_parser.add_argument("--status")

    delete_parser = subparsers.add_parser("delete", help="Delete an asset")
    delete_parser.add_argument("asset_id")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    storage_path = Path(__file__).resolve().parent.parent / "assets.json"
    manager = AssetManager(storage_path=storage_path)

    if args.command == "list":
        assets = manager.list_assets()
        if not assets:
            print("No assets found.")
            return

        for asset in assets:
            print(f"{asset.id}: {asset.name} | {asset.category} | {asset.value} | {asset.status}")

    elif args.command == "add":
        asset = manager.add_asset(args.name, args.category, args.value, args.status)
        print(f"Added asset {asset.id}")

    elif args.command == "update":
        updates = {}
        if args.name is not None:
            updates["name"] = args.name
        if args.category is not None:
            updates["category"] = args.category
        if args.value is not None:
            updates["value"] = args.value
        if args.status is not None:
            updates["status"] = args.status

        asset = manager.update_asset(args.asset_id, **updates)
        if asset is None:
            print("Asset not found")
        else:
            print(f"Updated asset {asset.id}")

    elif args.command == "delete":
        deleted = manager.delete_asset(args.asset_id)
        if deleted:
            print(f"Deleted asset {args.asset_id}")
        else:
            print("Asset not found")


if __name__ == "__main__":
    main()
