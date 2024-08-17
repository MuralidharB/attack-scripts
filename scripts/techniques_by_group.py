import argparse
import os
import json
import pandas as pd
import sys


parser = argparse.ArgumentParser(
                    prog='techniques_by_group',
                    description='List all techniques associated with a tactic')

parser.add_argument('tactic', choices= ['Reconnaissance', 'Resource Development', 'Initial Access',
                                        'Execution', 'Persistence', 'Privilege Escalation',
                                        'Defense Evasion', 'Credential Access, Discovery',
                                        'Lateral Movement', 'Collection', 'Command and Control',
                                        'Exfiltration', 'Impact',])

parser.add_argument('-g', '--group')

args = parser.parse_args()
print(args.tactic, args.group)

tactic = args.tactic.lower()
techniques_by_tactics = {}
with open("techniques_by_tactics.json") as f:
    for k, v in json.load(f).items():
        techniques_by_tactics[k] = []
        for i in v:
            techniques_by_tactics[k].append(i.split("techniques")[1].strip("/").replace("/", "."))

grps = pd.read_csv("groups.csv").sort_values("Group Name")

for grpname in grps["Group Name"].unique():
    grp_techniques = grps[grps["Group Name"] == grpname]
    for k, v in techniques_by_tactics.items():
        if k != tactic:
            continue
        print("============== %s ===============" % grpname)
        print("%s:" %k)
        print(",".join(["\"%s\""%i for i in grp_techniques.TID if os.path.exists("/Users/muralidharbalcha/src/atomic-red-team/atomics/%s" % i) and i in v]))

    #print("\n".join(["Get-AtomicTechnique -Path C:\\AtomicRedTeam\\atomics\\%s\%s.yaml" %(i, i ) for i in grp_techniques.TID if os.path.exists("/Users/muralidharbalcha/src/atomic-red-team/atomics/%s" % i)]))
