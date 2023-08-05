import os
import json
import multiprocessing
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from rcd_pyutils import decorator_manager


@decorator_manager.timeit(program_name="Parallel Writing to json")
def write_json_parallel(tuple_json: tuple, json_path: str) -> None:
    work_func = partial(write_json, output_path=json_path)
    with ThreadPoolExecutor() as executor:
        list(executor.map(work_func, tuple_json))


def write_json(tuple_json: tuple, output_path: str) -> None:
    json_id, json_content = tuple_json
    print(f"Generating {json_id}...")
    with open(os.path.join(output_path, f"{json_id}.json"), "w", encoding="utf8") as f:
        json.dump(json_content._asdict(), f, ensure_ascii=False)
