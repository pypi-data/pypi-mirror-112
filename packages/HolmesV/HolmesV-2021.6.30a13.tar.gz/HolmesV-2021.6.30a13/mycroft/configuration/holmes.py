"""This file will check a system level HolmesV specific config file

The file is json with comment support like the regular mycroft.conf

Default locations tried by order until a file is found
- /etc/HolmesV/holmes.conf
- /etc/mycroft/holmes.conf

XDG locations are then merged over the select default config (if found)

Default values:

{
   // the "name of the core",
   //         eg, OVOS, Neon, Chatterbox...
   //  all XDG paths should respect this
   //        {xdg_path}/{base_folder}/some_resource
   // "mycroft.conf" default paths are derived from this
   //        /opt/{base_folder}/mycroft.conf
   //        ~/.{base_folder}/mycroft.conf
   "base_folder": "mycroft",

   // the filename of "mycroft.conf",
   //      eg, ovos.conf, chatterbox.conf, neon.conf...
   // "mycroft.conf" default paths are derived from this
   //        /opt/{base_folder}/{config_filename}
   //        ~/.{base_folder}/{config_filename}
   "config_filename": "mycroft.conf",

   // override the default.conf location, allows changing the default values
   //     eg, disable backend, disable skills, configure permissions
   "default_config_path": null
}
"""
from mycroft.util.json_helper import load_commented_json, merge_dict
from os.path import isfile, dirname, join
from xdg import BaseDirectory as XDG


def get_holmes_config():
    config = {}
    if isfile("/etc/HolmesV/holmes.conf"):
        config = merge_dict(config,
                            load_commented_json("/etc/HolmesV/holmes.conf"))
    elif isfile("/etc/mycroft/holmes.conf"):
        config = merge_dict(config,
                            load_commented_json("/etc/mycroft/holmes.conf"))

    # This includes both the user config and
    # /etc/xdg/HolmesV/holmes.conf
    for p in XDG.load_config_paths("HolmesV"):
        if isfile(join(p, "holmes.conf")):
            config = merge_dict(config, join(p, "holmes.conf"))

    return {"base_folder": "mycroft",
            "config_filename": "mycroft.conf",
            "default_config_path": join(dirname(__file__), "mycroft.conf")}
