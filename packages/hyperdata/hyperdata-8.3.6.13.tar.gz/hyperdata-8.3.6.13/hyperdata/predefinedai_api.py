from .hyperdata_api import HyperdataApi
import os
import requests
from typing import Dict
import json
import pandas as pd
import argparse
import sys
import yaml


class PredefinedAIApi:
    def __init__(self):
        self.hd_api = HyperdataApi()
        if "webserver_addr" not in os.environ:
            self.is_local = True
        else:
            self.is_local = False

            self.server_addr = os.path.join(os.environ["webserver_addr"], "predefinedai", "v2")
            self.headers = {
                "Content-Type": "application/json",
                "Project-Id": os.environ["project_id"],
                "Token": os.environ["token"],
                "User-Id": os.environ["user_id"],
            }

    def get_model_infos(self):
        if not self.is_local:
            res = requests.get(
                os.path.join(
                    self.server_addr, "model", "?experiment_id=" + str(os.environ["experiment_id"]),
                ),
                headers=self.headers,
                verify=False,
            )
            return json.loads(res.text)
        else:
            print("Current mode is local, Skip get_model_infos.")

    def insert_model_info(
        self, model_name: str, algorithm: str, metric: str, metric_result: str, model_json: Dict,
    ) -> int:
        if not self.is_local:
            input_json = {
                "experiment_id": os.environ["experiment_id"],
                "workflow_id": os.environ["workflow_id"],
                "model_name": model_name,
                "algorithm": algorithm,
                "metric": metric,
                "metric_result": metric_result,
                "model_json": json.dumps(model_json),
            }
            res = requests.post(
                os.path.join(self.server_addr, "models"),
                headers=self.headers,
                data=json.dumps(input_json),
                verify=False,
            )
            if res.status_code != 200:
                raise Exception(f"status code {res.status_code} failed. {res.text}")
            model_dict = json.loads(res.text)
            return int(model_dict["id"])
        else:
            print("Current mode is local, Skip insert_model_info.")
            return 1

    def insert_visualizations(self, model_id: int, type: str, result: str) -> None:
        if not self.is_local:
            input_json = {
                "experiment_id": os.environ["experiment_id"],
                "model_id": model_id,
                "type": type,
                "result": result,
            }
            res = requests.post(
                os.path.join(self.server_addr, "visualization"),
                headers=self.headers,
                data=json.dumps(input_json),
                verify=False,
            )
            if res.status_code != 200:
                raise Exception(f"status code {res.status_code} failed. {res.text}")
        else:
            print("Current mode is local, Skip insert_visualizations.")

    def get_inference_csv_path(self):
        return os.path.join(self.hd_api.get_inference_path(), "inference.csv")

    def upload_inference_csv(self):
        if not self.is_local:
            if int(os.environ["target_do_id"]) == 0:
                print("target do id not selected. skip upload inference csv")
                return

            df = pd.read_csv(self.get_inference_csv_path(), index=False)
            df_json = df.to_json(orient="split")

            inf_data = {
                "columns": df_json["columns"],
                "data": df_json["data"],
                "experiment_id": os.environ["experiment_id"],
                "target_do_id": os.environ["target_do_id"],
                "is_truncated": os.environ["is_truncated"],
            }
            res = requests.post(
                url=os.path.join(self.server_addr, "inference"),
                headers=self.headers,
                data=json.dumps(inf_data),
                verify=False,
            )
            if res.status_code != 200:
                raise Exception(f"status code {res.status_code} failed. {res.text}")
        else:
            print("Current mode is local, Skip upload_inference_csv.")
            return ""


class PredefinedAIArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.predefinedai_args = {}
        self.predefinedai_support_args = (
            "PredefinedAIArgumentParser.int",
            "PredefinedAIArgumentParser.float",
            "PredefinedAIArgumentParser.str",
            "PredefinedAIArgumentParser.column",
            "PredefinedAIArgumentParser.columns",
            "PredefinedAIArgumentParser.bool",
        )
        self.predefinedai_inner_func = (
            "int_parse",
            "float_parse",
            "str_parse",
            "column_parse",
            "columns_parse",
            "bool_parse"
        )

    def add_argument(self, *args, **kwargs):
        if "action" in kwargs and kwargs["action"] == "help":
            super().add_argument(*args, **kwargs)
            return

        if "type" not in kwargs or not kwargs["type"][0].__name__ in self.predefinedai_inner_func:
            raise ValueError(f"type must be in {self.predefinedai_support_args}")

        if "action" in kwargs:
            raise ValueError(f"Cannot use action in PredefinedAIArgumentParser.")

        parse_func, local_params = kwargs["type"]
        kwargs["type"] = parse_func
        super().add_argument(*args, **kwargs)

        if not args[0].startswith("--"):
            raise ValueError("name must start with --")

        name = args[0][2:]
        default = None
        if "default" in kwargs:
            default = kwargs["default"]

        description = None
        if "help" in kwargs:
            description = kwargs["help"]
        else:
            description = ""

        required = None
        if "required" in kwargs:
            required = kwargs["required"]
        else:
            required = False

        choices = None
        if "choices" in kwargs:
            choices = kwargs["choices"]

        arg_dict = {
            "name": name,
            "default": default,
            "description": description,
            "required": required
        }
        if parse_func.__name__ == "int_parse":
            if default is None:
                default = local_params["max"] - local_params["min"]

            if choices is None and local_params["window"] == 0:
                raise ValueError("Please specify choices or window.")

            if choices is not None and local_params["window"] != 0:
                raise ValueError("Cannot use choices and window both.")

            arg_dict.update({
                "type": "int",
                "min": local_params["min"],
                "max": local_params["max"],
            })
            if choices is not None:
                arg_dict["choices"] = choices
            else:
                arg_dict["window"] = local_params["window"]
        elif parse_func.__name__ == "float_parse":
            if default is None:
                default = local_params["max"] - local_params["min"]

            if choices is None and local_params["window"] == 0.:
                raise ValueError("Please specify choices or window.")

            if choices is not None and local_params["window"] != 0.:
                raise ValueError("Cannot use choices and window both.")

            arg_dict.update({
                "type": "float",
                "min": local_params["min"],
                "max": local_params["max"],
            })
            if choices is not None:
                arg_dict["choices"] = choices
            else:
                arg_dict["window"] = local_params["window"]
        elif parse_func.__name__ == "str_parse":
            if default is None:
                default = ""

            arg_dict.update({
                "type": "str",
            })
            if choices is not None:
                arg_dict["choices"] = choices
        elif parse_func.__name__ == "column_parse":
            if default is None:
                default = ""

            arg_dict.update({
                "type": "column",
            })
        elif parse_func.__name__ == "columns_parse":
            if default is None:
                default = "[]"

            arg_dict.update({
                "type": "columns",
                "name": name,
                "default": default,
                "description": description,
                "required": required
            })
        elif parse_func.__name__ == "bool_parse":
            if default is None:
                default = True

            arg_dict.update({
                "type": "bool",
            })
        else:
            raise ValueError(f"parse function {parse_func.__name__} cannot found.")

        self.predefinedai_args[arg_dict["name"]] = arg_dict

    @staticmethod
    def int(
        min: int = 0,
        max: int = sys.maxsize,
        window: int = 1
    ):
        def int_parse(arg):
            try:
                val = int(arg)
            except ValueError:
                raise argparse.ArgumentTypeError(f"{arg} cannot cast to integer.")

            if min < max:
                raise ValueError(f"{min} must be less than {min}")
            elif val < min:
                raise ValueError(f"{arg} must be greater than {min}.")
            elif val > max:
                raise ValueError(f"{arg} must be less than {max}.")
            elif (val - min) % window != 0:
                raise ValueError(f"'({arg} - {min}) mod {window}' must be zero.")
            return val

        return int_parse, locals()

    @staticmethod
    def float(
        min: float = 0.,
        max: float = sys.float_info.max,
        window: float = 1.
    ):
        def float_parse(arg):
            try:
                val = float(arg)
            except ValueError:
                raise argparse.ArgumentTypeError(f"{arg} cannot cast to float.")

            if val < min:
                raise ValueError(f"{arg} must be greater than {min}.")
            elif val > max:
                raise ValueError(f"{arg} must be less than {max}.")
            elif (val - min) % window != 0.:
                raise ValueError(f"'({arg} - {min}) mod {window}' must be zero.")
            return val

        return float_parse, locals()

    @staticmethod
    def str():
        def str_parse(arg):
            try:
                val = str(arg)
            except ValueError:
                raise argparse.ArgumentTypeError(f"{arg} cannot cast to str.")

            return val

        return str_parse, locals()

    @staticmethod
    def column():
        def column_parse(arg):
            try:
                val = str(arg)
            except ValueError:
                raise argparse.ArgumentTypeError(f"{arg} cannot cast to str. column must be str.")

            return val

        return column_parse, locals()

    @staticmethod
    def columns():
        def columns_parse(arg):
            try:
                val = json.loads(arg)
            except Exception as e:
                print(e)
                raise argparse.ArgumentTypeError(f"{arg} cannot cast to dictionary. columns must be json string.")

            return val

        return columns_parse, locals()

    @staticmethod
    def bool():
        def bool_parse(arg):
            if isinstance(arg, bool):
                return arg
            if arg.lower() in ('yes', 'true', 't', 'y', '1'):
                return True
            elif arg.lower() in ('no', 'false', 'f', 'n', '0'):
                return False
            else:
                raise argparse.ArgumentTypeError('Boolean value expected.')

        return bool_parse, locals()

    def update_train_config(self, base_dir="../config"):
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir, exist_ok=True)

        train_config_path = os.path.join(base_dir, "train_config.yaml")
        args_list = [val for key, val in self.predefinedai_args.items()]
        if not os.path.isfile(train_config_path):
            train_dict = {
                "train": {
                    "model": "",
                    "pipeline_image_info": {
                        "name": "",
                        "task_type": "",
                        "image": "",
                        "image_pull_policy": "Always",
                        "cpu": "",
                        "memory": "",
                        "gpu": "",
                        "working_dir": "",
                        "args": {},
                        "envs": {},
                    }
                }
            }
            train_dict["train"]["pipeline_image_info"]["args"] = args_list
            with open(train_config_path, "w") as f:
                yaml.dump(train_dict, f)
        else:
            with open(os.path.join(train_config_path), "r+") as f:
                train_dict = yaml.safe_load(f)
                train_dict["train"]["pipeline_image_info"]["args"] = args_list
                yaml.dump(train_dict, f)
