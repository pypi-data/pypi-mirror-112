from typing import Dict
import os
import shutil
import subprocess
from uuid import uuid4
from aws_cdk import core
import aws_cdk.aws_lambda as lambda_


class AppLambdaLayer(lambda_.LayerVersion):

    def __init__(self, scope: core.Construct, construct_id: str,
                 build_path: str = None,
                 include: Dict[str, str] = None, **kwargs,
                 ):
        """
        :param scope:
        :param construct_id:
        :param build_path: Absolute build directory path
        :param include: Dictionary that maps absolute paths to be included to -> lambda layer paths
        :param kwargs: compatible_runtimes (required), ...
        """
        if build_path is None:
            build_path = "_build/" + uuid4().hex
        if include is None:
            include = {}

        # clean build path
        shutil.rmtree(build_path, ignore_errors=True)
        os.makedirs(build_path)

        # app lambda layer
        os.makedirs(f"{build_path}/app_lambda_layer/python")
        # app -> external requirements
        subprocess.run(f"poetry export -f requirements.txt > app_lambda_layer/requirements.txt", cwd=build_path, shell=True)
        subprocess.run(f"pip install -r app_lambda_layer/requirements.txt -t app_lambda_layer/python", cwd=build_path, shell=True)
        # app -> include paths
        for path in include:
            os.makedirs(f"{build_path}/app_lambda_layer/python/{include[path]}")
            shutil.copytree(path, f"{build_path}/app_lambda_layer/python/{include[path]}", dirs_exist_ok=True)

        # optimize (remove Lambda Runtime modules)
        lambda_included = [
            "boto3",
            "botocore",
            "s3transfer",
        ]
        for module in lambda_included:
            shutil.rmtree(f"{build_path}/app_lambda_layer/python/{module}", ignore_errors=True)

        super().__init__(
            scope,
            construct_id,
            code=lambda_.Code.from_asset(f"{build_path}/app_lambda_layer"),
            **kwargs,
        )
