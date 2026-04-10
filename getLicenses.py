import os
import json
import csv
import meraki
from decouple import config
from icecream import ic

API_KEY = config("API_KEY")
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

LICENSES_JSON_FOLDER = "./licenses_json"
LICENSES_CSV = "./csv/licenses.csv"


def get_all_organisations():
    try:
        return dashboard.organizations.getOrganizations()
    except Exception as e:
        ic(f"Error fetching organisations: {e}")
        return []


def get_license_overview(org_id):
    """Co-term licensing overview (expiry date, licensed device counts, etc.)."""
    try:
        return dashboard.organizations.getOrganizationLicensesOverview(org_id)
    except Exception as e:
        ic(f"Error fetching license overview for org {org_id}: {e}")
        return None


def get_per_device_licenses(org_id):
    """Per-device licenses (individual license keys and their assignments)."""
    try:
        return dashboard.organizations.getOrganizationLicenses(
            org_id, total_pages="all"
        )
    except Exception as e:
        ic(f"Error fetching per-device licenses for org {org_id}: {e}")
        return None


def save_to_json(data, filename, folder):
    if not data:
        ic(f"No data to save for {filename}. Skipping.")
        return
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    ic(f"Saved {file_path}")


def build_csv_rows(org_name, licensing_model, overview, per_device):
    """Return a list of flat dicts suitable for CSV export."""
    rows = []

    if licensing_model == "co-term" and overview:
        # One summary row per org for co-term
        row = {
            "org_name": org_name,
            "licensing_model": "co-term",
            "expiration_date": overview.get("expirationDate", ""),
            "status": overview.get("status", ""),
            "licensed_device_counts": json.dumps(
                overview.get("licensedDeviceCounts", {})
            ),
            "license_count": overview.get("licenseCount", ""),
            "license_key": "",
            "device_serial": "",
            "seat_count": "",
            "license_type": "",
        }
        rows.append(row)

    if per_device:
        for lic in per_device:
            row = {
                "org_name": org_name,
                "licensing_model": "per-device",
                "expiration_date": lic.get("expirationDate", ""),
                "status": lic.get("status", ""),
                "licensed_device_counts": "",
                "license_count": "",
                "license_key": lic.get("licenseKey", ""),
                "device_serial": lic.get("deviceSerial", ""),
                "seat_count": lic.get("seatCount", ""),
                "license_type": lic.get("licenseType", ""),
            }
            rows.append(row)

    return rows


CSV_FIELDS = [
    "org_name",
    "licensing_model",
    "expiration_date",
    "status",
    "licensed_device_counts",
    "license_count",
    "license_key",
    "device_serial",
    "seat_count",
    "license_type",
]


if __name__ == "__main__":
    organisations = get_all_organisations()
    os.makedirs("./csv", exist_ok=True)

    all_csv_rows = []

    for org in organisations:
        org_id = org["id"]
        org_name = org["name"]
        licensing_model = org.get("licensing", {}).get("model", "unknown")

        ic(f"Processing: {org_name} ({licensing_model})")

        overview = None
        per_device = None

        if licensing_model == "co-term":
            overview = get_license_overview(org_id)
        else:
            per_device = get_per_device_licenses(org_id)

        # Save raw JSON per org
        org_data = {
            "org_id": org_id,
            "org_name": org_name,
            "licensing_model": licensing_model,
            "overview": overview,
            "per_device_licenses": per_device,
        }
        safe_name = org_name.replace(" ", "_").replace("/", "_")
        save_to_json(org_data, f"Licenses_{safe_name}.json", LICENSES_JSON_FOLDER)

        rows = build_csv_rows(org_name, licensing_model, overview, per_device)
        all_csv_rows.extend(rows)

    # Write combined CSV
    with open(LICENSES_CSV, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(all_csv_rows)

    ic(f"CSV written to {LICENSES_CSV} ({len(all_csv_rows)} rows)")
