import sys
import requests

def gen_config_files(nodes, path):
    for node in nodes:
        if node["node_type"] == "dynamips":
            name = f'{node["node_type"]}-{node["name"]}'
            url = f"{FILES_ENDPOINT}/{node['node_type']}/{node['node_id']}/configs/i{node['properties']['dynamips_id']}_startup-config.cfg"
            config = requests.get(url).text
            print(url)
            with open(f"{path}/{name}.cfg", "w", newline="\n") as f:
                f.write(config)

url = "http://172.16.253.1:3080/v2/projects/f91df25f-ee34-4fdd-8567-4482894463a9/files/project-files/dynamips/02fed366-a956-4d86-b0b2-70a2d430318d/configs/i3_startup-config.cfg"

GNS3_SERVER_IP = "172.16.253.1"
GNS3_SERVER_PORT = "3080"

if len(sys.argv) < 3:
    print("Usage: python export_gns3_configs.py <project_id> <path>")
    sys.exit(1)

PROJECT_ID = sys.argv[1]

API_URL = f"http://{GNS3_SERVER_IP}:{GNS3_SERVER_PORT}/v2/"
NODES_ENDPOINT = f"{API_URL}projects/{PROJECT_ID}/nodes"
FILES_ENDPOINT = f"{API_URL}projects/{PROJECT_ID}/files/project-files"

path = sys.argv[2]

nodes = requests.get(NODES_ENDPOINT).json()

gen_config_files(nodes, path=path)