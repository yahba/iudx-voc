#!/usr/local/bin/python3
import json
import os
import glob

from collections import OrderedDict


classes_path = ["../../base-schemas/classes/", "../../data-models/classes/"]
properties_path = ["../../base-schemas/properties/", "../../data-models/properties/"]

if not os.path.exists("../../generated/"):
    os.makedirs("../../generated/")
expanded_path = "../../generated/"


def find(element, array):
    for item in array:
        if item['@id'] == element:
            return item

def generate(class_path, property_path):
    for class_file in glob.glob(os.path.join(class_path, '*.jsonld')):
        domain = class_file.replace(class_path, "")
        domain = domain.replace(".jsonld", "")
        domain = "iudx:" + domain
        with open(class_file, "r+") as class_obj:
            new_dict = OrderedDict()
            obj = json.load(class_obj)
            if "@context" in obj.keys():
                new_dict["@context"] = obj["@context"]
                del(obj["@context"])
            else:
                print("@context missing in " + class_file)
            if "@graph" in obj.keys():
                new_dict["@graph"] = obj["@graph"]
                del(obj["@graph"])
            else:
                print("@graph missing in " + class_file)
            for prop_file in glob.glob(os.path.join(property_path, '*.jsonld')):
                with open(prop_file, "r+") as prop_obj:
                    prop = json.load(prop_obj)
                    if "@graph" in prop.keys():
                        try:
                            includes = find(domain, prop["@graph"][0]["iudx:domainIncludes"])
                            if includes is not None:
                                new_dict["@graph"].append(prop["@graph"][0])
                        except KeyError:
                            pass
                            #print("iudx:domainIncludes not in " + prop_file)
                    else:
                        print("@graph missing in " + prop_file)
            os.makedirs(os.path.dirname(expanded_path), exist_ok=True)
            with open(expanded_path + domain.replace("iudx:", "") + ".jsonld", "w+") as new_file:
                json.dump(new_dict, new_file, indent=4)


if len(classes_path) == len(properties_path):
    for cpath, ppath in zip(classes_path, properties_path):
        generate(cpath, ppath)