import argparse
import os
import re
import sys
import traceback
import shutil
import subprocess

from environment import CondaEnvironment
from server import OmnisciServer
from utils import execute_process


def main():
    omniscript_path = os.path.dirname(__file__)
    script_path = os.path.join(omniscript_path, "run_ibis_tests.py")
    santander_path = os.path.join(omniscript_path, "santander")
    santander_data_dir = os.path.join(santander_path, "datasets")
    remove_datasets_dir = False
    data_file_path = "/localdisk/amyskov/benchmark_datasets/santander/train.csv"
    data_file_rows = [str(x * 10) + "k" for x in range(1, 20)]
    headed_data_files = [
        os.path.abspath(
            os.path.join(omniscript_path, "santander", "datasets", f"train{str(rows)}.csv")
        )
        for rows in range(20, 101, 20)
    ]
    head_data_file_cmd = [
        f"head ./santander/datasets/train.csv -n {rows * 1000} > ./santander/datasets/train{str(rows)}.csv".split()
        for rows in range(20, 101, 20)
    ]

    benchmark_cmd_template = [
        "python3",
        script_path,
        "-en",
        "amyskov-benches",
        "-ec",
        "True",
        "-s",
        "True",
        "-py",
        "3.7",
        "-task",
        "benchmark",
        "-table",
        "agent_test_ibis",
        "-ci",
        "/localdisk/amyskov/omniscripts/ci_requirements.yml",
        "-i",
        "/localdisk/amyskov/ibis/",
        "-executable",
        "/localdisk/amyskov/omniscidb_patched/build/bin/omnisci_server",
        "-bench_name",
        "santander",
        "-no_ml",
        "true",
        "-port",
        "61274",
        "-http_port",
        "61278",
        "-calcite_port",
        "61279",
        "-db_server",
        "ansatlin07.an.intel.com",
        "-db_port",
        "3306",
        "-db_pass",
        "omniscidb",
        "-db_name",
        "omniscidb",
        "-db_table_etl",
        "santander_etl_decimal",
        "-db_user",
        "gashiman",
        "-val",
        "true",
        "-import_mode",
        "copy-from",
    ]

    # "-no_pandas", "false",
    # "-iterations", "1",
    # "-data_file", "/localdisk/amyskov/benchmark_datasets/santander/train.csv",
    # "-dec_precision", "9",
    # "-dec_scale", "6",
    # "-parallel_validation", "true",
    # "-save_pd_etl_res", "true",
    # "-meas_set", "5"

    benchmark_cmd_val_append = [
        "-no_pandas",
        "false",
        "-iterations",
        "3",
        "-dec_precision",
        "8",
        "-dec_scale",
        "4",
    ]
    benchmark_cmd_val_serial = [
        benchmark_cmd_template
        + benchmark_cmd_val_append
        + ["-meas_set", "1", "-parallel_validation", "false", "-data_file", file_name]
        for file_name in headed_data_files
    ]
    benchmark_cmd_val_parallel = [
        benchmark_cmd_template
        + benchmark_cmd_val_append
        + ["-meas_set", "2", "-parallel_validation", "true", "-data_file", file_name]
        for file_name in headed_data_files
    ]

    benchmark_cmd_decimal_first_run = benchmark_cmd_template + [
        "-no_ibis",
        "true",
        "-save_pd_etl_res",
        "true",
        "-iterations",
        "1",
        "-dec_precision",
        "8",
        "-dec_scale",
        "4",
        "-meas_set",
        "0",
        "-data_file",
        data_file_path
    ]
    benchmark_cmd_decimal_append = [
        "-meas_set",
        "3",
        "-no_pandas",
        "true",
        "-iterations",
        "3",
        "-parallel_validation",
        "true",
        "-data_file",
        data_file_path,
        "-use_saved_pd_etl_res",
        "true",
    ]
    benchmark_cmd_decimal = [
        benchmark_cmd_template
        + benchmark_cmd_decimal_append
        + ["-dec_precision", str(number_precision), "-dec_scale", str(number_scale)]
        for number_precision in range(4, 11)
        for number_scale in range(2, 7)
        if number_precision - number_scale > 1
    ]

    conda_env_base = CondaEnvironment("base")

    try:
        conda_env_base.run(benchmark_cmd_decimal_first_run)
    except Exception as exc:
        print("CMD:", benchmark_cmd_decimal_first_run)
        print(exc)
        sys.exit(0)

    try:
        for cmd in benchmark_cmd_decimal:
            conda_env_base.run(cmd)
    except Exception as exc:
        print("CMD:", cmd)
        print(exc)
        sys.exit(0)


    try:
        if not os.path.exists(santander_data_dir):
            os.mkdir(santander_data_dir)
            shutil.copyfile(data_file_path, os.path.join(santander_data_dir, "train.csv"))

        for cmd in head_data_file_cmd:
            os.system(" ".join(cmd))

        for cmd in benchmark_cmd_val_serial:
            conda_env_base.run(cmd)

        for cmd in benchmark_cmd_val_parallel:
            conda_env_base.run(cmd)

    finally:
        if remove_datasets_dir:
            os.remove(santander_data_dir)


if __name__ == "__main__":
    main()
