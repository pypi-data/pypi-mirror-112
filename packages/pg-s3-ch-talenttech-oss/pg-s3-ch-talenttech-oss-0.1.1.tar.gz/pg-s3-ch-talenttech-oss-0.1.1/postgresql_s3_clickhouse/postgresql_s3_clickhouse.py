import os
import sys
import glob
import math
import gzip
import logging
import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta, time
from s3.client import Client as s3_client
from clickhouse_driver import Client


class PGS3CH:

    def __init__(self, config, entity, s3_config, ch_config, pg_config):

        self.ch_fields = {}
        self.entity_name = entity
        self.entity = config[entity]
        self.execution_date = os.getenv('execution_date')
        self.export_path = './csv'

        self.s3_config = s3_config
        self.pg_config = pg_config
        self.ch_config = ch_config

        if 'temp_table_prefix' in ch_config:
            self.temp_table_prefix = ch_config['temp_table_prefix']
        else:
            self.temp_table_prefix = '_temp_'

        self.connect_to_ch()

        try:
            logging.info('Working directory is {getcwd}'.format(getcwd=os.getcwd() ))
            os.makedirs(self.export_path)
        except OSError:
            logging.info('Can\'t create directory {export_path}'.format(export_path=self.export_path))
        else:
            logging.info('{export_path} was successfully created'.format(export_path=self.export_path))

    def get_table_schema_ch(self):
        sql = """select name, type, comment from system.columns where database='{database}' and table='{table}'
                AND name NOT IN ({exclude_columns})   """.format(database=self.entity['ch']['database'], table=self.entity['ch']['table'], exclude_columns=self.entity['ch']['exclude_columns'])

        logging.info(sql)
        result = self.ch_client.execute(sql)

        self.schema_pg_select_fields = {}
        self.schema_ch_insert_fields = []

        for row in result:
            if row[2].find('Exclude') == -1:
                self.schema_pg_select_fields[row[0]] = row[1]

            if row[2].find('#OnInsert:') > -1:
                start = row[2].find('#OnInsert:') + 10
                end = row[2].find(':EndOnInsert#')
                self.schema_ch_insert_fields.append(row[2][start:end])
            else:
                self.schema_ch_insert_fields.append(row[0])

        if len(self.schema_pg_select_fields) < 1:
            logging.info('CH schema error: {ch_fields}'.format(ch_fields=self.schema_pg_select_fields))
            exit(1)

        if len(self.schema_ch_insert_fields) < 1:
            logging.info('CH schema error: {ch_fields}'.format(ch_fields=self.schema_ch_insert_fields))
            exit(1)

        logging.info('CH schema for {database}.{table} - OK'.format(database=self.entity['ch']['database'], table=self.entity['ch']['table']) )

    def connect_to_ch(self):
        self.ch_client = Client(
            host=self.ch_config['host'],
            user=self.ch_config['user'],
            password=self.ch_config['password'],
            database=self.ch_config['database']
        )

    def connect_to_pg(self):
        cnx = psycopg2.connect(user=self.pg_config['user'],
                               password=self.pg_config['password'],
                               host=self.pg_config['host'],
                               port=self.pg_config['port'],
                               database=self.pg_config['database'],
                               sslmode='disable')

        cnx.set_client_encoding('UTF8')
        return cnx

    def extract_updated(self):

        cnx = self.connect_to_pg()

        cursor = cnx.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        range_from = datetime.combine(datetime.fromisoformat(self.execution_date).date(), time())

        parts = self.entity['pg']['range_parts_per_day']

        for k in range(0, parts):
            range_to = range_from + timedelta(seconds=3600*24/parts-0.000001)

            sql = self.entity['pg']['sql'].format(fields=','.join(self.ch_fields.keys()), range_from=range_from, range_to=range_to)
            logging.info(sql.strip())

            with gzip.open('./csv/{entity_name}_{range_from}.csv.gz'.format(entity_name=self.entity_name,
                                                                            range_from=str(range_from).replace(' ', '_')), 'wt') as fa:
                cursor = cnx.cursor()
                cursor.copy_to(fa, '({sql})'.format(sql=sql), null='')
                cursor.close()

            range_from = range_from + timedelta(hours=24/parts)

        cursor.close()
        cnx.close()

        logging.info('extract_updated finished')

    # TODO: step добавить в конфиг
    def extract_full(self, step=500000):

        logging.info('Starting full extract')
        cnx = self.connect_to_pg()

        cursor = cnx.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        sql = self.entity['pg']['sql_history_range']
        cursor.execute(sql)
        for row in cursor:
            min_id = row['min_id']
            max_id = row['max_id']
        cursor.close()

        logging.info('Min ID: {min_id}'.format(min_id=min_id))
        logging.info('Max ID: {max_id}'.format(max_id=max_id))

        if 'sql_history_step' in self.entity['pg']:
            step = self.entity['pg']['sql_history_step']

        end = math.ceil(max_id / step)
        logging.info('Range from 0 to {end}, multiply by {step}'.format(end=end, step=step))

        for id in range(0, end):

            range_from = min_id + id * step
            range_to = min_id + id * step + step - 1

            sql = self.entity['pg']['sql_history'].format(fields=','.join(self.schema_pg_select_fields.keys()), range_from=range_from, range_to=range_to)

            logging.info(sql)

            with gzip.open('./csv/{entity_name}_{range_from}.csv.gz'.format(entity_name=self.entity_name, range_from=range_from), 'wt') as fa:
                time_start = (datetime.now())
                cursor = cnx.cursor()
                cursor.copy_to(fa, '({sql})'.format(sql=sql), null='')
                cursor.close()
                time_end = (datetime.now())
                logging.info('Time elapsed: ' + str(time_end-time_start))

        cnx.close()

        logging.info('Full extract finished')

    # TODO: Что делать с PARTITION?
    def create_temporary_table(self):
        #sql = 'CREATE TABLE {database}._temp_{table} ENGINE=MergeTree() PARTITION BY tuple() ORDER BY tuple() AS SELECT * FROM {database}.{table} LIMIT 0'.format(database=self.entity['ch']['database'], table=self.entity['ch']['table'])
        sql = """CREATE TABLE {staging_database}.{temp_table_prefix}{table} ON CLUSTER '{{cluster}}' AS {database}.{table} 
                    ENGINE=ReplicatedMergeTree() 
                    PARTITION BY tuple() 
                    ORDER BY {key_field}""".format(staging_database=self.entity['ch']['staging_database'],
                                                   temp_table_prefix=self.temp_table_prefix,
                                                   database=self.entity['ch']['database'],
                                                   table=self.entity['ch']['table'],
                                                   key_field=self.entity['key_field'])
        logging.info(sql)
        self.ch_client.execute(sql)

    def drop_temporary_table(self):
        sql = """DROP TABLE IF EXISTS {staging_database}.{temp_table_prefix}{table} ON CLUSTER '{{cluster}}'""".format(staging_database=self.entity['ch']['staging_database'],
                                                                                                                       temp_table_prefix=self.temp_table_prefix,
                                                                                                                       table=self.entity['ch']['table'])
        self.ch_client.execute(sql)
        logging.info(sql)

    def optimize(self):
        sql = """SELECT partition, count() cnt from system.parts where database='{database}' and table='{table}' and active
                GROUP BY partition 
                having cnt > 1""".format(database=self.entity['ch']['database'], table=self.entity['ch']['table'])
        result = self.ch_client.execute(sql)

        for row in result:
            logging.info('Partition {partition} has {parts} parts'.format(partition=row[0], parts=row[1]) )
            sql_optimize = """OPTIMIZE TABLE {database}.{table} ON CLUSTER '{{cluster}}' PARTITION {partition} """.format(database=self.entity['ch']['database'], table=self.entity['ch']['table'], partition=row[0])
            logging.info(sql_optimize)
            self.ch_client.execute(sql_optimize)
            logging.info('OK')

    def s3_to_temp(self):

        schema = []
        schema_insert = []

        for k in self.schema_pg_select_fields:
            schema.append(k + ' ' + self.schema_pg_select_fields[k])

        for k in self.schema_ch_insert_fields:
            schema_insert.append(k)

        logging.info('Copying from {s3_endpoint_url}/{bucket} to {database}.{temp_table_prefix}{table}'.format(s3_endpoint_url=self.s3_config['S3_ENDPOINT_URL'],
                                                                                                               bucket=self.s3_config['S3_TOPMIND_CLIENT_DATA_BUCKET'],
                                                                                                               database=self.entity['ch']['database'],
                                                                                                               temp_table_prefix=self.temp_table_prefix,
                                                                                                               table=self.entity['ch']['table']
                                                                                                               ))

        sql = """
            INSERT INTO {staging_database}.{temp_table_prefix}{table}
            SELECT 
                {schema_insert}, NOW()
            FROM s3("{endpoint_url}/{bucket}/{upload_path}/{entity_name}_*.csv.gz", 
                    '{S3_ACCESS_KEY}',
                    '{S3_ACCESS_SECRET}',
                    'TSV', 
                    '{schema}',
                    'gzip'
                    );
            """.format(staging_database=self.entity['ch']['staging_database'],
                       table=self.entity['ch']['table'],
                       temp_table_prefix=self.temp_table_prefix,
                       endpoint_url=self.s3_config['S3_ENDPOINT_URL'],
                       bucket=self.s3_config['S3_TOPMIND_CLIENT_DATA_BUCKET'],
                       upload_path=self.s3_config['UPLOAD_PATH'],
                       S3_ACCESS_KEY=self.s3_config['S3_ACCESS_KEY'],
                       S3_ACCESS_SECRET=self.s3_config['S3_ACCESS_SECRET'],
                       entity_name=self.entity_name,
                       schema=', '.join(schema),
                       schema_insert=', '.join(schema_insert)
                       )

        logging.info(sql)

        self.ch_client.execute(sql)

        logging.info('Loading from S3 successful')

    def load_to_s3(self):

        logging.info('Copying to S3: {}'.format(self.s3_config['S3_ENDPOINT_URL']))

        client = s3_client(
            aws_access_key_id=self.s3_config['S3_ACCESS_KEY'],
            aws_secret_access_key=self.s3_config['S3_ACCESS_SECRET'],
            endpoint_url=self.s3_config['S3_ENDPOINT_URL'],
            bucket=self.s3_config['S3_TOPMIND_CLIENT_DATA_BUCKET'],
        )

        files = [f for f in glob.glob("csv/{entity_name}_*.csv.gz".format(entity_name=self.entity_name), recursive=False)]

        for file in files:
            logging.info(os.path.basename(file))
            client.upload_file(file, '{upload_path}/{filename}'.format(upload_path=self.s3_config['UPLOAD_PATH'], filename=os.path.basename(file)), print_progress=False)

        logging.info('Copied to S3')

    def copy_prod_to_temp(self):

        sql = """
                INSERT INTO {staging_database}.{temp_table_prefix}{table}
                SELECT * FROM {database}.{table} WHERE {primary_key_field} NOT IN (SELECT {primary_key_field} FROM {staging_database}.{temp_table_prefix}{table})
                """.format(staging_database=self.entity['ch']['staging_database'],
                           temp_table_prefix=self.temp_table_prefix,
                           database=self.entity['ch']['database'],
                           table=self.entity['ch']['table'],
                           primary_key_field=self.entity['key_field'])

        logging.info(sql)
        self.ch_client.execute(sql)

    def exchange_temp_to_prod(self):

        sql = """EXCHANGE TABLES {staging_database}.{temp_table_prefix}{table} AND {database}.{table} ON CLUSTER '{{cluster}}' """.format(staging_database=self.entity['ch']['staging_database'],
                                                                                                                                          temp_table_prefix=self.temp_table_prefix,
                                                                                                                                          database=self.entity['ch']['database'],
                                                                                                                                          table=self.entity['ch']['table'])

        logging.info(sql)
        self.ch_client.execute(sql)