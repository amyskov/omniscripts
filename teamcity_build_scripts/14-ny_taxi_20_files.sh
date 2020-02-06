ROOT_DIR="${PWD}"
cd omniscripts
python3 run_omnisci_benchmark.py -m dataset -path="${ROOT_DIR}"/omniscidb/Benchmarks -u admin -p HyperInteractive -e "${ROOT_DIR}"/omniscidb/build/bin/omnisci_server --port 61274 -n omnisci -t taxi_benchmark -l taxi_test -f '/localdisk/benchmark_datasets/taxi/trips_xa{a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t}.csv.gz' -c "${ROOT_DIR}"/omniscidb/Benchmarks/import_table_schemas/taxis.sql -d "${ROOT_DIR}"/omniscidb/Benchmarks/queries/taxis -i 5 -fs 5000000 -db-server=ansatlin07.an.intel.com -db-user=gashiman -db-pass=omniscidb -db-name=omniscidb -db-table=taxibench --env_name ${ENV_NAME} --env_check True --save_env True --ci_requirements ci_requirements.yml -commit ${BUILD_REVISION}
