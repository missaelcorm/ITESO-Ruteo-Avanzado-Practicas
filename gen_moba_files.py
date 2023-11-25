import sys
import requests
import json

def gen_moba_files(name, console, path):
    name = f'{node["node_type"]}-{node["name"]}'
    console = node["console"]
    template = f"{name} = #98#1%{GNS3_SERVER_IP}%{console}%%%2%%%%%0%0%%1080%%#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%0%_Std_Colors_0_%80%24%0%1%-1%<none>%%0%0%-1%0#0# #-1"
    
    with open(f"{path}/{name}.moba", "w", newline="\n") as f:
        f.write(template)

def gen_mobaxterm_mxt_sessions(nodes, path):
    template = f"""[Bookmarks]
SubRep=GNS3
ImgNum=41"""

    for node in nodes:
        name = f'{node["name"]}-{node["node_type"]}'
        console = node["console"]
        node_template = f"{name} = #98#1%{GNS3_SERVER_IP}%{console}%%%2%%%%%0%0%%1080%%#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%0%_Std_Colors_0_%80%24%0%1%-1%<none>%%0%0%-1%0#0# #-1"
        template += f"\n{node_template}"
        
    with open(f"{path}/GNS3.mxtsessions", "w", newline="\n") as f:
        f.write(template)

if len(sys.argv) != 3:
    print("Usage: python gen_moba_files.py <project_id> <path>")
    exit(1)        

GNS3_SERVER_IP = "172.16.253.1"
GNS3_SERVER_PORT = "3080"
PROJECT_ID = sys.argv[1]

API_URL = f"http://{GNS3_SERVER_IP}:{GNS3_SERVER_PORT}/v2/"
NODES_ENDPOINT = f"{API_URL}projects/{PROJECT_ID}/nodes"

path = sys.argv[2]

nodes = requests.get(NODES_ENDPOINT).json()
desired_keys = ["name", "console", "node_type"]
print(json.dumps(nodes, indent=2))
new_nodes = []

for node in nodes:
    if node["node_type"] in ["dynamips", "vpcs"]:
        new_node = {key: node[key] for key in desired_keys}
        new_nodes.append(new_node)

# print(json.dumps(new_nodes, indent=2))

# for node in new_nodes:
#     gen_moba_files(node["name"], node["console"], path=path)

gen_mobaxterm_mxt_sessions(new_nodes, path=path)