#!/usr/local/bin/python3
import json
import os
import glob
import copy
import sys


folder_path = "../../generated/"
if not os.path.exists("../../class_markdowns/"):
    os.makedirs("../../class_markdowns/")
markdown_path = "../../class_markdowns/"

def graph(obj):
    if "@graph" in obj.keys():
        graph_obj = copy.deepcopy(obj["@graph"])
        for i in obj["@graph"]:
            if isinstance(i["@type"], list):
                typ = i["@type"][0].split(":")
                if typ[1] == "Class":
                    class_name = i["@id"].replace(":", "_")
                    print("class " + class_name + "{", file=text_file) 
                    for j in graph_obj:
                        for prop in j["@type"]:
                            if "Property" in prop:
                                print("\t" + j["@id"].replace(":", "_"), file=text_file)
                            elif "Relationship" in prop:
                                print("\t" + j["@id"].replace(":", "_"), file=text_file)
                    print("}", file=text_file)
                    try:
                        superclass_name = i["rdfs:subClassOf"]["@id"].replace(":", "_")
                        super_class = i["rdfs:subClassOf"]["@id"]
                        if "rdf:" not in super_class:
                            super_class = super_class.split(":")
                            with open(folder_path + super_class[1] + ".jsonld", "r+") as super_file:
                                super_obj = json.load(super_file)
                                graph(super_obj)
                        print(superclass_name + " --|> " + class_name + " : SubClass", file=text_file)
                    except KeyError:
                        pass
            elif "Class" in i["@type"]:
                typ = i["@type"].split(":")
                if typ[1] == "Class":
                    class_name = i["@id"].replace(":", "_")
                    print("class " + class_name + "{", file=text_file) 
                    for j in graph_obj:
                        for prop in j["@type"]:
                            if "Property" in prop:
                                print("\t" + j["@id"].replace(":", "_"), file=text_file)
                            elif "Relationship" in prop:
                                print("\t" + j["@id"].replace(":", "_"), file=text_file)
                    print("}", file=text_file)
                    try:
                        superclass_name = i["rdfs:subClassOf"]["@id"].replace(":", "_")
                        super_class = i["rdfs:subClassOf"]["@id"]
                        if "rdf:" not in super_class:
                            super_class = super_class.split(":")
                            with open(folder_path + super_class[1] + ".jsonld", "r+") as super_file:
                                super_obj = json.load(super_file)
                                graph(super_obj)
                        print(superclass_name + " --|> " + class_name + " : SubClass", file=text_file)
                    except KeyError:
                        pass
    else:
        print("@graph missing in " + filename)

for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
    with open(filename, "r+") as obj_file:
         obj = json.load(obj_file)
         with open(markdown_path + filename.replace("../../generated/", "").replace(".jsonld", ".txt"), "w+") as text_file:
             print("@startuml\n", file=text_file)
             graph(obj)
             print("\n@enduml", file=text_file)