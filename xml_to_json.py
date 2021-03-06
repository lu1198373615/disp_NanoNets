import os
import json
from xmljson import parker
from xml.etree.ElementTree import fromstring
import argparse

def keep_keys(old_dict):
  new_dict = {}
  for key in old_dict:
    if key in ["object","segmented","size"]:
      new_dict[key]=old_dict[key]
  return new_dict


parser = argparse.ArgumentParser(description='Convert xml Annotations to json annotations')
parser.add_argument('--xml', type=str,  metavar='path/to/input/xml/', default=r'F:\ML_homework_data/xmls/', help='(default "annotations/xmls/") path to xml annotations')
parser.add_argument('--json', type=str,  metavar='path/to/output/json/', default=r'F:\ML_homework_data/jsons/', help='(default "annotations/json/") path to out json annotations')

parser.print_help()
print("\n")

args = vars(parser.parse_args())

input_directory = r'H:\homework_data\xmls'
output_directory = r'H:\homework_data\jsons'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

all_input_files = os.listdir(input_directory)
xml_input_files = [file for file in all_input_files if file.endswith(".xml")]
for xml_file in xml_input_files:
  f = open(os.path.join(input_directory, xml_file),"rb")
  json_output = json.dumps(keep_keys(parker.data(fromstring(f.read()))))
  f.close()

  f = open(os.path.join(output_directory, xml_file.replace(".xml",".json")),"w")
  output = json.loads(json_output)
  output.setdefault('object',[])
  this_obj = output["object"]
  if type(this_obj)!=type([]):
    this_obj = [this_obj]
  f.write(json.dumps(this_obj))
  f.close()