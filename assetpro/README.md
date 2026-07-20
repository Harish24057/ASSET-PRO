# Asset Pro

Asset Pro is a simple Python starter project for tracking assets such as laptops, vehicles, or equipment.

## Features
- Add assets
- List stored assets
- Update asset details
- Delete assets
- Persist data to a JSON file

## Run locally

```bash
python -m asset_pro list
python -m asset_pro add --name "Laptop" --category "IT" --value 1200
```

## Run tests

```bash
python -m unittest discover -s tests -v
```
