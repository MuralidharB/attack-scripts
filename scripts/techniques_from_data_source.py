from stix2 import TAXIICollectionSource, Filter
from taxii2client.v20 import Collection
import argparse
import pandas as pd

# Establish TAXII2 Collection instance for Enterprise ATT&CK collection
collection = Collection("https://cti-taxii.mitre.org/stix/collections/95ecc380-afe9-11e4-9b6c-751b66dd541e/")
# Supply the collection to TAXIICollection
tc_src = TAXIICollectionSource(collection)

def data_sources():
    """returns all data sources in Enterprise ATT&CK"""

    all_data_srcs = []

    # Get all techniques in Enterprise ATT&CK
    techniques = tc_src.query([Filter("type", "=", "attack-pattern")])

    # Get all data sources in Enterprise ATT&CK
    for tech in techniques:
        if 'x_mitre_data_sources' in tech:
            all_data_srcs += [
                data_src for data_src in tech.x_mitre_data_sources
                if data_src not in all_data_srcs
            ]
    
    return all_data_srcs

def techniques(data_source):
    """returns all techniques which contain the given data source."""
    
    techs_with_data_src = tc_src.query([
        Filter("type", "=", "attack-pattern"),
        Filter("x_mitre_data_sources", "in", data_source)
    ])

    return techs_with_data_src

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetches the current ATT&CK STIX 2.0 objects from the ATT&CK TAXII server, prints all of the data sources listed in Enterprise ATT&CK, and then lists all the Enterprise techniques containing a given data source."
    )
    parser.add_argument("-data_source",
        type=str,
        default="User Account: User Account Creation",
        help="the datasource by which to filter techniques. Default value is '%(default)s'."
    )

    args = parser.parse_args()

    #print("All data sources in Enterprise ATT&CK:\n")
    #print("\n".join(data_sources()))
    #print("\n")
    
    # get techniques from the specified data source
    technique_list = techniques(args.data_source)

    # Get names of techniques
    print(f"The following {len(technique_list)} techniques use '{args.data_source}' as a data source:\n")
    techs = []
    for tech in technique_list:
        techs.append({"name": tech.name, "url":tech.external_references[0].url, "id":tech.external_references[0].external_id})

    pd.DataFrame(techs).to_csv("techniques.csv") 
