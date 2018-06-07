# FAIRDATAintegrationtest

Testing Environment for Integration testing:

    Python framework unittests has been used to implement integration testing
    Environment includes Fairdata services: IDA, Metax, Estin and Dpres   

The testing environment contains all tests and related utilities and resources used to validate proper behavior and functionality of the FAIDATA service following modifications to its implementation and/or configuration. Each service has its own subdirectory containg test cases specific to the service (for example: /ida/ida.py, /metax/metax.py, /etsin/etsin.py). 
The test cases between services can be found in main directory (for example: /ida-metax.py, /metax-etsin.py). Name of the file indicates the services the test cases belongs. run_all.py is the main file that runs all the tests. 

Configuration

github repository of test environment: https://github.com/CSCfi/FAIRDATAtest

to run the test

    git clone https://github.com/CSCfi/FAIRDATAtest ./fairdatatest
    pip install -r requirements.txt
    cd faidatatest
    mkdir config
    cp template/config.py config/config.py
    vi config/config.py 

Run tests

Execute the following command to run all the test cases:

python -W ignore run_all.py

Commands to run tests of specific component:

Nextcloud: python -W ignore nextcloud_test.py

Ida-metax: python -W ignore ida_metax.py

metax-etsin: python -W ignore metax_etsin.py

metax-dpres: python -W ignore metax_dpres.py 
