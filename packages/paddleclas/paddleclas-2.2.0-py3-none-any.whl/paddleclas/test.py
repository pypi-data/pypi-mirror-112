import os
import sys
__dir__ = os.path.dirname(__file__)
sys.path.append(os.path.join(__dir__, ""))
sys.path.append(os.path.join(__dir__, "deploy"))

import argparse

from deploy.utils import config



def args_cfg():
    parser = config.parser()
    other_options = [("infer_imgs", str, None, "help"), ("model_name", str, None, "help"), ("use_gpu", bool, True, "help")]
    for name, opt_type, deault, description in other_options:
        parser.add_argument("--"+name, type=opt_type, default=deault, help=description)

    args = parser.parse_args()

    for name, opt_type, deault, description in other_options:
        args.override.append(f"{name}={eval('args.'+name)}")

    cfg = config.get_config(
        args.config, overrides=args.override, show=args.verbose)

    return cfg


cfg = args_cfg()
print(cfg)