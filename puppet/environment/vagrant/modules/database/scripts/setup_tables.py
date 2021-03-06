#!/usr/bin/python

'''

This file initializes the following database tables within the
'db_machine_learning' database:

    @tbl_dataset_entity, record the dataset instance, and the corresponding
        userid who created, or modified the information, and the model type.

        @tbl_feature_count, record the number of features expected within an
            observation, with respect to a given 'id_entity'.

        @tbl_svm_data, records a tuple of observation-feature values
        @tbl_svr_data, records a tuple of criterion-predictor values

            - observation label: synonymous to dependent variable label, and
                can be 'NULL' if the 'criterion value' is defined.
            - criterion value: can be 'NULL' if the 'observation label' is
                defined.
            - feature label / value: synonymous to independent variable label,
                or predictor label.

        @model_type, reference table containing all possible model types.

        @tbl_observation_label, record every unique observation label, with respect
            to a given 'id_entity'.

    @tbl_svm_results, record svm prediction result, with respect to the
        following linked tables:

        @tbl_svm_results_class, record predicted classes, with respect to to a
            given 'id_result'.
        @tbl_svm_results_probability, record predicted probabilities, with
            respect to a given 'id_result'.
        @tbl_svm_results_decision_function, record predicted decisision
            function, with respect to a given 'id_result'.

    @tbl_svm_results, record svr prediction result, with respect to the
        following linked tables:

        @tbl_svr_results_results_r2, record predicted r^2, with respect to a
            given 'id_result'.

'''

import yaml
from sys import argv
import MySQLdb as DB


# local variables
#
# @argv[1], first passed-in argument from command (argv[0] is the filename),
#     indicating the project root directory.
#
# @argv[2], second passed-in argument from command, or boolean value
#     indicating if build is vagrant instance.
if argv[2] == 'true':
    prepath = argv[1]
else:
    prepath = argv[1] + '/test'

# define configuration
with open(prepath + '/hiera/settings.yaml', 'r') as stream:
    # local variables
    settings = yaml.load(stream)
    models = settings['application']['model_type']
    host = settings['general']['host']
    db_ml = settings['database']['name']
    provisioner = settings['database']['provisioner']
    provisioner_password = settings['database']['provisioner_password']

    # create connection
    conn = DB.connect(
        host,
        provisioner,
        provisioner_password,
        db_ml
    )

    with conn:
        # create cursor object
        cur = conn.cursor()

        # create 'tbl_user'
        sql_statement = '''\
                        CREATE TABLE IF NOT EXISTS tbl_user (
                            id_user INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR (50) NOT NULL,
                            email VARCHAR (255) NOT NULL,
                            password VARCHAR (1069) NOT NULL,
                            datetime_joined DATETIME NOT NULL,
                            INDEX (username)
                        );
                        '''
        cur.execute(sql_statement)

        # create 'tbl_feature_count'
        sql_statement = '''\
                        CREATE TABLE IF NOT EXISTS tbl_feature_count (
                            id_size INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            id_entity INT NOT NULL,
                            count_features INT NOT NULL,
                            INDEX (id_size)
                        );
                        '''
        cur.execute(sql_statement)

        # create 'tbl_dataset_entity'
        sql_statement = '''\
                        CREATE TABLE IF NOT EXISTS tbl_dataset_entity (
                            id_entity INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            title VARCHAR (50) NOT NULL,
                            model_type INT NOT NULL,
                            uid_created INT NOT NULL,
                            datetime_created DATETIME NOT NULL,
                            uid_modified INT NULL,
                            datetime_modified DATETIME NULL,
                            INDEX (id_entity)
                        );
                        '''
        cur.execute(sql_statement)

        # create 'tbl_observation_label'
        sql_statement = '''\
                        CREATE TABLE IF NOT EXISTS tbl_observation_label (
                            id_label INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            id_entity INT NOT NULL,
                            dep_variable_label VARCHAR(75) NOT NULL,
                            INDEX (id_label)
                        );
                        '''
        cur.execute(sql_statement)

        # create 'tbl_svm_data'
        sql_statement = '''\
                        CREATE TABLE IF NOT EXISTS tbl_svm_data (
                            id_value INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            id_entity INT NOT NULL,
                            dep_variable_label VARCHAR (50) NOT NULL,
                            indep_variable_label VARCHAR (50) NOT NULL,
                            indep_variable_value FLOAT NOT NULL,
                            INDEX (id_value)
                        );
                        '''
        cur.execute(sql_statement)

        # create 'tbl_svr_data'
        sql_statement = '''\
                        CREATE TABLE IF NOT EXISTS tbl_svr_data (
                            id_value INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            id_entity INT NOT NULL,
                            criterion VARCHAR (50) NOT NULL,
                            indep_variable_label VARCHAR (50) NOT NULL,
                            indep_variable_value FLOAT NOT NULL,
                            INDEX (id_value)
                        );
                        '''
        cur.execute(sql_statement)

        # create 'tbl_model_type'
        sql_statement = '''\
                        CREATE TABLE IF NOT EXISTS tbl_model_type (
                            id_model INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            model VARCHAR (50) NOT NULL,
                            INDEX (id_model)
                        );
                        '''
        cur.execute(sql_statement)

        # populate 'tbl_model_type'
        sql_statement = '''\
                        INSERT INTO tbl_model_type (model) VALUES (%s);
                        '''
        cur.executemany(sql_statement, models)

        # create 'tbl_svm_results'
        sql_statement = '''\
                        CREATE TABLE IF NOT EXISTS tbl_svm_results (
                            id_result INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            title VARCHAR (50) NOT NULL,
                            result VARCHAR (30) NOT NULL,
                            uid_created INT NOT NULL,
                            datetime_created DATETIME NOT NULL,
                            INDEX (title)
                        );
                        '''
        cur.execute(sql_statement)

        # create 'tbl_svm_results_class'
        sql_statement = '''\
                        CREATE TABLE IF NOT EXISTS tbl_svm_results_class (
                            id_class INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            id_result INT NOT NULL,
                            class VARCHAR (50) NOT NULL
                        );
                        '''
        cur.execute(sql_statement)

        # create 'tbl_svm_results_probability'
        sql_statement = '''\
                        CREATE TABLE IF NOT EXISTS tbl_svm_results_probability (
                            id_probability INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            id_result INT NOT NULL,
                            probability FLOAT NOT NULL
                        );
                        '''
        cur.execute(sql_statement)

        # create 'tbl_svm_results_decision_function'
        sql_statement = '''\
                        CREATE TABLE IF NOT EXISTS tbl_svm_results_decision_function (
                            id_decision_function INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            id_result INT NOT NULL,
                            decision_function FLOAT NOT NULL
                        );
                        '''
        cur.execute(sql_statement)

        # create 'tbl_svr_results'
        sql_statement = '''\
                        CREATE TABLE IF NOT EXISTS tbl_svr_results (
                            id_result INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            title VARCHAR (50) NOT NULL,
                            result VARCHAR (30) NOT NULL,
                            uid_created INT NOT NULL,
                            datetime_created DATETIME NOT NULL,
                            INDEX (title)
                        );
                        '''
        cur.execute(sql_statement)

        # create 'tbl_svr_results_r2'
        sql_statement = '''\
                        CREATE TABLE IF NOT EXISTS tbl_svr_results_r2 (
                            id_r2 INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            id_result INT NOT NULL,
                            r2 FLOAT NOT NULL
                        );
                        '''
        cur.execute(sql_statement)
