python3 run_ibis_tests.py --env_name ${ENV_NAME} --env_check True --python_version 3.7 --task benchmark --ci_requirements "${PWD}"/ci_requirements.yml --save_env True --report "${PWD}"/.. --ibis_path "${PWD}"/../ibis/ --executable "${PWD}"/../omniscidb/build/bin/omnisci_server -u admin -p HyperInteractive -n agent_test_ibis --bench_name santander --dpattern '/localdisk/benchmark_datasets/santander/train.csv.gz' --iters 5 -db-server ansatlin07.an.intel.com -db-port 3306 -db-user gashiman -db-pass omniscidb -db-name omniscidb -db-table santander_ibis -commit_omnisci ${BUILD_REVISION} -commit_ibis ${BUILD_IBIS_REVISION}