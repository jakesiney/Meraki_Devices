import os
import json
import meraki
from decouple import config
from icecream import ic

# Assuming you have the API key and org_id set up
API_KEY = config("API_KEY")
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

def get_all_organisations():
    """Fetch all organisations."""
    try:
        organisations = dashboard.organizations.getOrganizations()
        return organisations
    except Exception as e:
        ic(f"Error fetching organisations: {e}")
        return []

def get_all_networks(org_id):
    """Fetch all networks for a given organization."""
    try:
        networks = dashboard.organizations.getOrganizationNetworks(
            org_id, total_pages="all"
        )
        return networks
    except Exception as e:
        ic(f"Error fetching networks for org {org_id}: {e}")
        return None

def get_all_devices(org_id):
    """Fetch all devices for a given organization."""
    try:
        devices = dashboard.organizations.getOrganizationDevices(
            org_id, total_pages="all"
        )
        return devices
    except Exception as e:
        ic(f"Error fetching devices for org {org_id}: {e}")
        return None

def get_devices_in_network(network_id):
    """Fetch devices in a specific network."""
    try:
        devices = dashboard.networks.getNetworkDevices(network_id)
        return devices
    except Exception as e:
        ic(f"Error fetching devices for network {network_id}: {e}")
        return None

def save_to_json(data, filename, folder):
    """Save data to a JSON file in the specified folder."""
    if data is None or not data:
        ic(f"No data to save for {filename}. Skipping file creation.")
        return
    
    try:
        # Ensure the folder exists
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Create the full file path
        file_path = os.path.join(folder, filename)
        
        # Save the data to the JSON file
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        ic(f"Data saved to {file_path}")
    except Exception as e:
        ic(f"Error saving data to {file_path}: {e}")

if __name__ == "__main__":
    # Fetch all organizations
    organisations = get_all_organisations()
    save_to_json(organisations, "AllOrganisations.json", "./organisations_json")

    # Iterate through each organization
    for org in organisations:
        org_id = org["id"]
        org_name = org["name"]

        # Fetch and save devices
        devices = get_all_devices(org_id)
        save_to_json(devices, f"Devices_in_{org_name.replace(' ', '_')}.json", "./devices_json")

        # Fetch and save networks
        networks = get_all_networks(org_id)
        save_to_json(networks, f"Networks_in_{org_name.replace(' ', '_')}.json", "./networks_json")