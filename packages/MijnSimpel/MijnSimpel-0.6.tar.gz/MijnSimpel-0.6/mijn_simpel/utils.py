import json
import yaml


def to_yaml_str(json_obj):
    yaml_obj = yaml.load(json.dumps(json_obj), Loader=yaml.SafeLoader)
    return yaml.dump(yaml_obj, default_flow_style=False)


def fmt_output(json_output, json_obj):
    if json_output:
        return json.dumps(json_obj)
    else:
        return to_yaml_str(json_obj)
