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

if [ $1 == "--help" ] || [ $1 == "-h" ] || [ $# -lt 5 ]; then 
	display_usage
	exit 0
else
    TEST_TYPE=$1
    CONTRACT_TYPE=$2
    SYMBOL=$3
    ASSET=$4
    PLATFORM=$5

    [ $TEST_TYPE == "TU" ] || [ $TEST_TYPE == "TV" ] || [ $TEST_TYPE == "ALL" ] && echo "TEST_TYPE = ${TEST_TYPE}" || exit 1
    [ $CONTRACT_TYPE == "SPOT" ] || [ $CONTRACT_TYPE == "FUTURES" ] || [ $CONTRACT_TYPE == "ALL" ] && echo "CONTRACT_TYPE = ${CONTRACT_TYPE}" || exit 1
    [ $SYMBOL == "BTC" ] || [ $SYMBOL == "ETH" ] || [ $SYMBOL == "BNB" ] || [ $SYMBOL == "ALL" ] && echo "SYMBOL = ${SYMBOL}" || exit 1
    [[ $ASSET == "USDT" ]] && echo "ASSET = ${ASSET}" || exit 1
    [ $PLATFORM == "BINANCE" ] || [ $PLATFORM == "ALL" ] && echo "PLATFORM = ${PLATFORM}" || exit 1
    
fi

rm -rf build/
path="./tests/"
cmd_symbol=${SYMBOL}${ASSET}
cmd_asset=${ASSET}

test_type=$(convert2lower ${TEST_TYPE})
platform=$(convert2lower ${PLATFORM})
contract_type=$(convert2lower ${CONTRACT_TYPE})

if [ $TEST_TYPE != "ALL" ] && [ $CONTRACT_TYPE != "ALL" ] && [ $PLATFORM != "ALL" ]; then
    build_dir="build/${test_type}"
    mkdir -p ${build_dir}
    path="${path}/${test_type}/${platform}/${contract_type}_tests.py"
    output_file="${build_dir}/${test_type}_${contract_type}.xml"

    SCRIPT_DIR=${PWD}/scripts/ CEPS_DIR=${PWD}/scripts/ceps/ \
    SYMBOL=${cmd_symbol} ASSET=${ASSET} \
    python3 -m pytest ${path} -v
    #python3 -m pytest --junitxml ${output_file} ${path} -v
    
    
    #rm -rf tmp/
elif [ $TEST_TYPE == "ALL" ] && [ $CONTRACT_TYPE == "ALL" ] \
  && [ $PLATFORM == "ALL" ] && [ $SYMBOL == "ALL" ]; then
    ################################### TU #####################################
        #TO MODIF
        declare -a test_type=("tu")
        declare -a platform_list=("binance")
        declare -a contract_type_list=("futures" "spot")
        declare -a cmd_symbol_list=("BTCUSDT" "ETHUSDT" "BNBUSDT")

        ######################### SPOT ##########################
        
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
                done

                #Gather all .xml in one
                output_file="${build_dir}/${test_type}_${contract_type}.xml"
                xmlmerge ${build_dir}/*.xml > ${output_file}

                mv ${output_file} ./docs/pages
            done
        done

    ################################### TV #####################################
    test_type="TV"
    #TO UPDATE

    #TO UPDATE WHEN TV ARE READY
    if [ ${TEST_TYPE} == "TV" ]; then
        echo "Concatener fichier xml en 1 pour mesure de couverture"
    fi
fi

#SCRIPT_DIR=$PWD/scripts/ CEPS_DIR=$PWD/scripts/ceps/ SYMBOL=BTCUSDT ASSET=USDT python3 -m pytest tests/tu/binance/spot_tests.py -v

#OLD
#TU
#python3 -m pytest --junitxml tests/results/tu_spot.xml tests/tu/spot_tests.py -vxk "not test_compute_side"
#python3 -m pytest --junitxml tests/results/tu_futures.xml tests/tu/futures_tests.py -vxk "not test_compute_side"
#rm .coverage.cloud*

#TV
#coverage run -m pytest --junitxml tests/results/tv_spot.xml tests/tv/spot_tests.py -vxk "not test_compute_side"
#coverage run -m pytest --junitxml tests/results/tv_futures.xml tests/tv/futures_tests.py -vxk "not test_compute_side"
#coverage combine; coverage report
#rm .coverage

# GENERATE DOC
# DEPENDANCES
#pip3 install -U sphinx; pip3 install sphinx_rtd_theme;pip3 install sphinx-test-reports

#cd docs; sphinx-apidoc -o . .. ; make html; cd ..