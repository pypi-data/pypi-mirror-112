# import os
# import json
# from functools import partial
# from concurrent.futures import ThreadPoolExecutor
#
# import pandas as pd
#
# from rcd_pyutils import decorator_manager
#
#
# @decorator_manager.timeit(program_name="Parallel Writing to json")
# def pandas_to_json(df: pd.DataFrame, json_path: str) -> None:
#     json_str = df.to_json(orient='records')
#     json_obj = json.loads(json_str)
#     iter_row = zip(df.index.tolist(), df.itertuples(index=False))
#     work_func = partial(write_json, output_path=json_path)
#     with ThreadPoolExecutor() as executor:
#         list(executor.map(work_func, iter_row))
