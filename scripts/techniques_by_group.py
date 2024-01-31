import os
import json
import pandas as pd

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
        if k != "discovery":
            continue
        print("============== %s ===============" % grpname)
        print("%s:" %k)
        print(",".join(["\"%s\""%i for i in grp_techniques.TID if os.path.exists("/Users/muralidharbalcha/src/atomic-red-team/atomics/%s" % i) and i in v]))

    #print("\n".join(["Get-AtomicTechnique -Path C:\\AtomicRedTeam\\atomics\\%s\%s.yaml" %(i, i ) for i in grp_techniques.TID if os.path.exists("/Users/muralidharbalcha/src/atomic-red-team/atomics/%s" % i)]))
