import pandas as pd
import yaml

from fiddler.core_objects import ModelInfo
from fiddler.fiddler_api import FiddlerApi
from fiddler.utils import cast_input_data


def execute_cmd(args):
    client = FiddlerApi(url=f'http://localhost:{args.port}', org_id=args.org)
    df = pd.read_csv('dataset.csv')
    with open('model.yaml') as input:
        model_info = ModelInfo.from_dict(yaml.safe_load(input))
        df = cast_input_data(df, model_info)
        if args.index:
            df = df.loc[[int(args.index)]]
        else:
            df = df.head()
        print('Input: ')
        print(df)
        result = client.run_model(args.project, args.model, df)
        print('Result: ')
        print(result)


def explain_cmd(args):
    client = FiddlerApi(url=f'http://localhost:{args.port}', org_id=args.org)
    df = pd.read_csv('dataset.csv')
    with open('model.yaml') as input:
        model_info = ModelInfo.from_dict(yaml.safe_load(input))
        df = cast_input_data(df, model_info)
        if args.index:
            df = df.loc[[int(args.index)]]
        else:
            df = df.head(1)
        print('Input: ')
        print(df)
        result = client.run_explanation(
            args.project, args.model, df, dataset_id='titanic'
        )
        print('Output: ')
        print(result)
