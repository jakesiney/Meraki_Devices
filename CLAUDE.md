# Meraki Devices

Python tooling to query the Cisco Meraki Dashboard API and export device/network inventory across multiple client organizations.

## Setup

Requires Python 3.12. Install dependencies:

```bash
uv sync
```

Run any script with:

```bash
uv run python <script>.py
```

Dependencies: `meraki`, `python-decouple`, `icecream`

Config is loaded from `.env`:
```
API_KEY=<meraki_api_key>
ORG_ID=<org_id>  # only needed for getAllOrgMerakiDevices.py
```

## Scripts

| Script | Purpose |
|--------|---------|
| `getAllMerakiDevices.py` | Fetches all orgs, then devices + networks per org. Saves to `organisations_json/`, `devices_json/`, `networks_json/` |
| `getAllOrgMerakiDevices.py` | Single-org variant — uses `ORG_ID` from `.env`. Saves `AllOrgNetworks.json` and `AllOrgDevices.json` to project root |
| `createCSV.py` | Converts all JSON files in `devices_json/` to CSV files in `./csv/` |
| `getLicenses.py` | Fetches license info for every org. Handles both co-term (overview) and per-device models. Saves per-org JSON to `licenses_json/` and a combined CSV to `csv/licenses.csv` |

## Output structure

```
organisations_json/   # AllOrganisations.json
devices_json/         # Devices_in_<OrgName>.json per org
networks_json/        # Networks_in_<OrgName>.json per org
licenses_json/        # Licenses_<OrgName>.json per org
csv/                  # CSV exports from devices_json/ and licenses.csv
```
