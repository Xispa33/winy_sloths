#!/bin/bash

display_usage() { 
	echo "This script is responsible for WS tests." 
	echo -e "\nUsage: \$0 [TEST_TYPE] [CONTRACT_TYPE] [SYMBOL] [ASSET] [PLATFORM]" 
    echo -e "       \$1 [TEST_TYPE] either TU, TV or ALL"
    echo -e "       \$2 [CONTRACT_TYPE] either SPOT, FUTURES or ALL"
    echo -e "       \$3 [SYMBOL] either BTC, ETH, BNB or ALL"
    echo -e "       \$4 [ASSET] has to be set to USDT"
    #TO UPDATE IN ELSE STATEMENT 
    echo -e "       \$5 [PLATFORM] either binance or bybit"
    echo -e "Examples: "
} 

convert2lower() {
    string=$1
    echo "${string}" | tr '[:upper:]' '[:lower:]'
}
convert2upper() {
    string=$1
    echo "${string}" | tr '[:lower:]' '[:upper:]'
}

if [ $1 == "--help" ] || [ $1 == "-h" ] || [ $# -lt 5 ]; then 
	display_usage
	exit 0
else
    TEST_TYPE=$1
    CONTRACT_TYPE=$2
    SYMBOL=$3
    ASSET=$4
    PLATFORM=$5

    [ $TEST_TYPE == "TU" ] || [ $TEST_TYPE == "TV" ] && echo "TEST_TYPE = ${TEST_TYPE}" || exit 1
    [ $CONTRACT_TYPE == "SPOT" ] || [ $CONTRACT_TYPE == "FUTURES" ] || [ $CONTRACT_TYPE == "ALL" ] && echo "CONTRACT_TYPE = ${CONTRACT_TYPE}" || exit 1
    [ $SYMBOL == "BTC" ] || [ $SYMBOL == "ETH" ] || [ $SYMBOL == "BNB" ] || [ $SYMBOL == "ALL" ] && echo "SYMBOL = ${SYMBOL}" || exit 1
    [[ $ASSET == "USDT" ]] && echo "ASSET = ${ASSET}" || exit 1
    [ $PLATFORM == "BINANCE" ] || [ $PLATFORM == "BYBIT" ] || [ $PLATFORM == "ALL" ] && echo "PLATFORM = ${PLATFORM}" || exit 1
    
fi

#rm -rf build/
path="./tests/"
if [ $SYMBOL != "ALL" ]; then
    cmd_symbol=${SYMBOL}${ASSET}
fi
cmd_asset=${ASSET}
test_type=$(convert2lower ${TEST_TYPE})
platform=$(convert2lower ${PLATFORM})
contract_type=$(convert2lower ${CONTRACT_TYPE})

declare -a test_type=($test_type)

if [ $CONTRACT_TYPE == "ALL" ]; then
    declare -a contract_type_list=("futures" "spot")
else
    declare -a contract_type_list=(${contract_type})
fi
if [ $SYMBOL == "ALL" ]; then
    #declare -a cmd_symbol_list=("BTCUSDT" "ETHUSDT" "BNBUSDT")
    declare -a cmd_symbol_list=("BTCUSDT")
else
    declare -a cmd_symbol_list=(${cmd_symbol})
fi
if [ $PLATFORM == "ALL" ]; then
    declare -a platform_list=("binance" "bybit")
else
    declare -a platform_list=(${platform})
fi

        ######################### TU ##########################
if [ ${TEST_TYPE} == "TU" ]; then        
    for platform in "${platform_list[@]}"
    do
        for contract_type in "${contract_type_list[@]}"
        do
            build_dir="build/${test_type}/${contract_type}/"
            mkdir -p ${build_dir}
            for cmd_symbol in "${cmd_symbol_list[@]}"
            do
                file_path="./tests/${test_type}/${platform}/${contract_type}_tests.py"
                output_file="${build_dir}/${test_type}_${contract_type}_${platform}_${cmd_symbol}.xml"
                SCRIPT_DIR=${PWD}/scripts/ CEPS_DIR=${PWD}/scripts/ceps/ \
                SYMBOL=${cmd_symbol} ASSET=${ASSET} \
                python3 -m pytest --junitxml ${output_file} ${file_path} -v
                cp ${output_file} ./docs/pages
            done

            #Gather all .xml in one
            #output_file="${build_dir}/${test_type}_${contract_type}.xml"
            #echo "Merging : ${contract_type}"
            #xmlmerge ${build_dir}/* > ${output_file}

            
        done
    done

        ######################### TV ##########################
elif [ ${TEST_TYPE} == "TV" ]; then
    if [ $PLATFORM == "ALL" ]; then
        declare -a platform_list=("binance")
    fi
    #Créer arbo en début de test
    for platform in "${platform_list[@]}"
    do
        build_dir="build/${test_type}/${contract_type}/"
        mkdir -p ${build_dir}
        mkdir -p ${PWD}/build/coverage
        for contract_type in "${contract_type_list[@]}"
        do
            mkdir -p ${PWD}/tests/tv/TESTS/${platform}/${contract_type}
            master=${platform}
            strat_filename="strat_test.txt"
            if [ ${platform} == "binance" ]; then
                master="Binance"
                slave="Bybit"
                API_KEY_MASTER_SPOT=`echo ${API_KEY_MASTER_SPOT_1}`
                API_SECRET_KEY_MASTER_SPOT=$(echo ${API_KEY_MASTER_SECRET_SPOT_1})
                API_KEY_MASTER_FUTURES=`echo ${API_KEY_MASTER_FUTURES_1}`
                API_SECRET_KEY_MASTER_FUTURES=$(echo ${API_KEY_MASTER_SECRET_FUTURES_1})
                API_KEY_SLAVE_SPOT=$(echo ${API_KEY_MASTER_SPOT_2})
                API_SECRET_KEY_SLAVE_SPOT=$(echo ${API_KEY_MASTER_SECRET_SPOT_2})
                API_KEY_SLAVE_FUTURES=$(echo ${API_KEY_MASTER_SPOT_2})
                API_SECRET_KEY_SLAVE_FUTURES=$(echo ${API_KEY_MASTER_SECRET_SPOT_2})
            else
                master="Bybit"
                slave="Binance"
                API_KEY_MASTER_SPOT=$(echo ${API_KEY_MASTER_SPOT_2})
                API_SECRET_KEY_MASTER_SPOT=$(echo ${API_KEY_MASTER_SECRET_SPOT_2})
                API_KEY_MASTER_FUTURES=$(echo ${API_KEY_MASTER_SPOT_2})
                API_SECRET_KEY_MASTER_FUTURES=$(echo ${API_KEY_MASTER_SECRET_SPOT_2})
                API_KEY_SLAVE_SPOT=${API_KEY_MASTER_SPOT_1}
                API_SECRET_KEY_SLAVE_SPOT=$(echo ${API_KEY_MASTER_SECRET_SPOT_1})
                API_KEY_SLAVE_FUTURES=`echo ${API_KEY_MASTER_FUTURES_1}`
                API_SECRET_KEY_SLAVE_FUTURES=$(echo ${API_KEY_MASTER_SECRET_FUTURES_1})
            fi
            # This account is always slave
            API_KEY_SLAVE_FUTURES_BINANCE=$(echo ${API_KEY_SLAVE_FUTURES_1})
            API_SECRET_KEY_SLAVE_FUTURES_BINANCE=$(echo ${API_KEY_SLAVE_SECRET_FUTURES_1})
            contract=$(convert2upper ${contract_type})
            if [ ${contract} == SPOT ]; then
                API_KEY_MASTER=${API_KEY_MASTER_SPOT}
                API_SECRET_KEY_MASTER=${API_SECRET_KEY_MASTER_SPOT}
                API_KEY_SLAVE=${API_KEY_SLAVE_SPOT}
                API_SECRET_KEY_SLAVE=${API_SECRET_KEY_SLAVE_SPOT}
            else
                API_KEY_MASTER=${API_KEY_MASTER_FUTURES}
                API_SECRET_KEY_MASTER=${API_SECRET_KEY_MASTER_FUTURES}
                API_KEY_SLAVE=${API_KEY_SLAVE_FUTURES}
                API_SECRET_KEY_SLAVE=${API_SECRET_KEY_SLAVE_FUTURES}
            fi
            echo -e "${master} ${API_KEY_MASTER} ${API_SECRET_KEY_MASTER} OUT ${contract} BTCUSDT\n0\n${slave} ${API_KEY_SLAVE} ${API_SECRET_KEY_SLAVE} OUT" > ${PWD}/tests/tv/TESTS/${platform}/${contract_type}/${strat_filename}
            #\n${master} ${API_KEY_SLAVE_FUTURES_BINANCE} ${API_SECRET_KEY_SLAVE_FUTURES_BINANCE} OUT
            chmod 777 ${PWD}/tests/tv/TESTS/${platform}/${contract_type}/${strat_filename}
            file_path="./tests/${test_type}/${contract_type}_tests.py"
            output_file="${build_dir}/${test_type}_${contract_type}_${platform}_${cmd_symbol}.xml"
            SCRIPT_DIR=${PWD}/scripts/ CEPS_DIR=${PWD}/scripts/ceps/ PLATFORM=${platform} \
            STRAT_FILENAME=${strat_filename} PYTHONPATH=${PWD}/conf coverage run \
            --rcfile=${PWD}/conf/.coveragerc -m pytest --junitxml \
            ${output_file} ${file_path} -vx
            
        done
    done
    mv .coverage* build/coverage
    cd build/coverage; coverage combine; coverage xml -i; 
    sed -i "s|/home/bl/actions-runner/_work/winy_sloths/winy_sloths/||g" coverage.xml
    cd ../..
fi