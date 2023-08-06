Amocrm custom library
==========

1. Retrieving data from amocrm amocrm.api (v2 and v4).
2. Uploading data to database. 

Supported databases:
-------------
* clickhouse
* vertica 


Usage
```sh
pip3 install amocrm-talenttech-oss
```

Retrieving data from API:
-------------

```python
import datetime
from api.api_loader_amocrm_v4 import AmocrmApiLoader as ApiLoaderV4

 
date_modified_from = datetime.datetime.now() - datetime.timedelta(days=1) #
args_api = {
                "amocrm_api_url": "https://<NAMESPACE>.amocrm.ru/amocrm.api/v4/<ENTITY>?page={page}&limit={limit}",
                "AUTH_URL":"https://<NAMESPACE>.amocrm.ru/oauth2/access_token",
                "CLIENT_SECRET":"xxxx",
                "CLIENT_ID": "xxx-xxx-xxxx-xxxx-xxxxxxx",
                "REDIRECT_URL":"https://xxxx/xx"
           }

args_s3 = {
                "aws_access_key_id": <S3_ACCESS_KEY>,
                "aws_secret_access_key":  <S3_ACCESS_SECRET>,
                "endpoint_url": <S3_ENDPOINT_URL>,
                "bucket": <S3_BUCKET>
          }



api_loader = ApiLoaderV4(
                entity=<ENTITY>,                # leads/tasks/companies or e.t.c
                s3_path=<S3_PATH>,              # this s3 folder should contain retrieved files
                s3_token_path=<S3_TOKEN_PATH>,  # directory for tokens
                args_s3=args_s3,
                args_api=args_api,
                date_modified_from=date_modified_from, #parameters is optional, if want load only updated records from date
                with_offset=True, 
                batch_api=500
            )

api_loader.auth(<CODE_AUTH>) #call it if you need to create or regenerate refresh token the first time
api_loader.extract()      
```


Uploading data to vertica:
-------------
```python
from db.vertica_uploader import UploaderDB as VerticaUploaderDB
sql_credentials = {
                "database": <DATABASE>,
                "schema": <SCHEMA>
                "user": <VERTICA_WRITE_USER>,
                "host": <VERTICA_HOST>,
                "port": <VERTICA_PORT>,
                "password": <VERTICA_WRITE_PASSWORD>,
                "vertica_configs": <VERTICA_CONFIGS>,
            }

args_s3 = {
                "aws_access_key_id": <S3_ACCESS_KEY>,
                "aws_secret_access_key":  <S3_ACCESS_SECRET>,
                "endpoint_url": <S3_ENDPOINT_URL>,
                "bucket": <S3_BUCKET>
          }        

db_uploader = VerticaUploaderDB(
            args_s3=args_s3,
            s3_path=s3_path,
            sql_credentials=sql_credentials,
            entity=<ENTITY>,
            table_name=<TABLE_NAME>,
            json_columns=[<COLUM_JSON_1>, <COLUM_JSON_2>]
        )
db_uploader.load_s3_to_db()        
```
  
Extract or load data to db:
-------------  
```python
import os
import json
args = {
    "action": os.getenv("action"),
    "etl_name_no_version": os.getenv("ETL_NAME_NO_VERSION"),
    "execution_date": parse(os.getenv("execution_date")),
    "config_name": os.getenv("config_name"),
    "entity": os.getenv("entity"),
    "args_s3": args_netology_s3,
    "sql_credentials": sql_credentials,
    "db": os.getenv("db"),
    "table_name": os.getenv("table_name"),
    "table_to_optimize": os.getenv("table_to_optimize"),
    "json_columns": os.getenv("json_columns"),
    "amocrm_secrets": json.loads(os.getenv("AMOCRM_TOKEN_SECRET")),
    "amocrm_api_url": os.getenv("amocrm_api_url"),
    "if_modified_since": os.getenv("if_modified_since"),
    "parser": os.getenv("parser"),
}

   amo_runner = AmocrmRunner(**args)
   #amo_runner.regenerate_file_secret(code_auth="def502003cdbc2c012e210f69190133bf1943b5ebf825ef46c10b52c077064e3b9cf1378831d6f28855b9e17e4c0f95e40213af8994c1e0fadd9221730219d3e54a5dcdf1f25a90a83a19cf4edb05bd024595eec042ec3c1170f78de9dd33b5074c72e9b1821d8db0c2b31e1ab82012e6f3361ee90283e88a0c95e61802cc4e46e8d3797d04d074f367c3162879bedd0fac4c6951faf73e27895f141769a77794de56abf940c3bd68f64b7cc959017767c421c618d0100ab4c4ec651bcb03a105b3fb9ae9a26fc46252dac707963c283d1cca7fd5ec29c6f384467b1d7090b8770b2b9c69a284cbd9f7548f4c7a4f5f00a229322ae68073b603b41eeece7162f46a7519d818c8d9ffb6c93e80fadc9a3db9e83f0e4af0f3965d43e81e48a868821c2d851e1b96ffb80a875f3ff211188a12054efdd1ccc93c4b2dd73d524671c8d8aca3b1c414bfda9d011801a2aeba0dc79f882f248788553b4e5a2d7f648c89b53d86079ef09ae13dfab0cea8ab4f137579eb128a270a2cf62487b65ffc57372bed6a4fb62635f0d7275b0eba18d64900a3ea6cac403f7949617bbba7ef6afa7b0e359c8b5daac05fd30c194575c253933a8d45ad8b8737842d57ceca1810da7797b23") #if secret file is empty or you net to create it the first time
   amo_runner.run()
```