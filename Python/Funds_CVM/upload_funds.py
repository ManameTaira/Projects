import re
from pandas.core.indexes import extension
import requests
import io
from zipfile import ZipFile
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import sqlalchemy as db
from sqlalchemy.dialects.mysql import insert
from dateutil.parser import parse


def create_datatable(engine, metadata, datatable_structure, table_name):
    """Create a table in the database connected by the engine and
    following the datatable_structure, the table name will be the table_name

    Args:
        engine (Engine obj): The connection to the database.
        metadata (MetaData obj): A collection of Table obj and their associated schema constructs.
        datatable_structure (list): A list where each element is a Column obj with the structure setted.
        table_name (str): The new table name.

    Returns:
        Table obj: A Table obj that represents the database table.
    """
    table = db.Table(table_name, metadata, *datatable_structure)
    metadata.create_all(engine)

    return table

def get_table(engine, datatable_structure, table_name):
    """Get the Table obj that represents the table table_name in the database.

    Args:
        engine (Engine obj): The connection to the database.
        datatable_structure (list): A list where each element is a Column obj with the structure setted.
        table_name (str): The table name.

    Returns:
        Table obj: A Table obj that represents the database table.
    """
    metadata = db.MetaData()

    return db.Table(table_name, metadata, autoload=True, autoload_with=engine) \
           if table_name in db.inspect(engine).get_table_names() \
           else create_datatable(engine, metadata, datatable_structure, table_name)                                                                     # if the table exists in the database return the obj, else create a new table in the database and return the new table obj                                                                 # check if the table_name is a table in the schema, if it is return the Table obj, else creat the table and return the Table obj created


def get_last_update_date(engine, table):
    """Get the date of the last update in the table.

    Args:
        engine (Engine obj): The connection to the database.
        table (Table obj): A obj taht represents the table in database.

    Returns:
        tuple of datetime: The date that was made the last insert/update in the table or None if there is no data in the table and
                           the max quota date in the datatable or None if there is no data in the table.
    """
    result = engine.execute(db.select([db.func.max(table.columns.date), db.func.max(table.columns.quota_date)])).fetchall()

    return result[0]


def request_get(url):
    """Execute the request using the method GET to the url and check if the status code 200 OK

    Args:
        url (str): The url to make the request.

    Raises:
        Exception: If the status code from the request is not 200.

    Returns:
        requests obj: The request result.
    """
    result = requests.get(url)

    if result.status_code != 200:
        raise Exception(f'Request could not return status code 200. Status code returned: {result.status_code}')

    return result


def parse_html_table(html, pattern):
    """Parse the html table to get the file last modified date, the file url and the data that the file refers to.

    Args:
        html (requests obj): The request result.
        pattern (str): A regex pattern to find the file in the html.
    Returns:
        matrix: A list of truples containing the file last update date (datetime), the file url (str) and the date that the file refers to (datetime).
    """
    table = []

    for row in BeautifulSoup(html.text, 'html.parser').find_all('tr'):
        if not (file:=re.search(pattern, row.text)):                                                                                                    # if the row text containg a match to the pattern, then it has a file link
            continue

        table.append((parse(row.find('td', class_='indexcollastmod').text).date(),                                                                      # the file last modified date
                      f'{html.url}{file.group(0)}',                                                                                                     # file full url
                      parse(f'{file.group(1)[:4]}-{file.group(1)[4:]}', default=datetime.date(2005, 1, 1))))                                            # the data that the file refers to, is in the file name, like inf_diario_fi_2005 -> datetime(2005, 1, 1) and inf_diario_fi_201703.csv -> datetime(2017, 3, 1)

    return table


def get_url_files_list(parser_parametters, last_update_date, max_quota_date):
    """Get a list of url to the files containing the data.

    Args:
        parser_parametters (dict): A dict containing the period as key ("historical" or "current") and the a dict containing the parametters to
                                   insert in the parse_html_table function.
        last_update_date (datetime or None): The date that was made the last insert/update in the table or None if the table is empty
        max_quota_date (datetime or None): The max quota date in the table.

    Returns:
        list: A list of url to the files.
    """
    url_files_list = []

    for _, param in parser_parametters.items():
        for last_update, file_url, file_date in parse_html_table(**param):
            if last_update_date is not None and last_update_date >= last_update and max_quota_date >= file_date:
                continue

            url_files_list.append(file_url)

    return url_files_list



def handle_files(url_file):
    """Handle both zip files and csv files.

    Args:
        url_file (str): The url to the file.

    Returns:
        tuple: A list containg the file url, None and the file extension if its a csv or
               a list containin the file names in the zip, the file zip obj and the file extension
    """
    if (file_extension := url_file.split('.')[-1]) == 'csv':
        return [url_file], None, file_extension                                                                                                         # it is a csv file, then it don have a zip obj to extract the file

    if file_extension  == 'zip':
        zip_file = ZipFile(io.BytesIO(request_get(url_file).content), 'r')                                                                              # download the zip file to the memory and read the zip
        return  zip_file.filelist, zip_file, file_extension                                                                                             # return the list of files inside the zip and the zip obj.

    raise Exception(f'Can not handle the file extension {file_extension}, check if the file is correct in the url.')


def download_data(url_files):
    """Download the data from the files to the memory

    Args:
        url_files_list (list): A list containing the urls to the files.

    Yields:
        byte: A byte value containing the data form the csv file.
    """
    for url_file in url_files:
        files_list, zip_file, file_extension = handle_files(url_file)

        for file in files_list:
            print(file)
            yield zip_file.read(file.filename) \
                  if file_extension == 'zip' \
                  else request_get(url_file).content                                                                                                    # if it is a zip file extract the csv file from the zip obj, else it is a csv file, then download the csv file to the memory


def get_data(url_files_list, rename_cols, csv_parse={'sep': ';'}, df_replace={'to_replace': None, 'value': None}):
    """Download the file to the memory and get the data from the csv file to a DataFrame.

    Args:
        url_files_list (list): A list containing the urls to the files.
        rename_cols (dict): A dict containing the csv column name as key and the table columns name as value.
        csv_parse (dict, optional): A dict containing the parameters as key end the value as key to parse the csv file to the DataFrame.
                                    Defaults to {'sep': ';'}. See the reference at
                                    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
        df_replace (dict, optional): A dict containing the parameters as key end the value as key to replace values in the DataFrame.
                                     Defaults to {'to_replace': None, 'value': None}. See reference at
                                     https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.replace.html
    Yields:
        DataFrame obj: A DataFrame containing the data from the csv, the columns name is the same as the SQL table.
    """

    for csv in download_data(url_files_list):
        df = pd.read_csv(io.BytesIO(csv), **csv_parse).replace(**df_replace)

        yield df.rename(columns=rename_cols)


def format_data(df, fill_na={}):
    """Format the data to be inserted in the database.

    Args:
        df (DataFrame obj): A DataFrame containing the data to be upload to the datatable.
        fill_na (dict): A dict containing the SQL column name as key and the value to fill if nan value in the df.
    Returns:
        list : A list of dict containing the column name as key and the value to upload as value.
    """
    return [{key: value if not pd.isna(value) else fill_na.get(key) for key, value in zip(df.columns, row)} for row in df.values.tolist()]


def upload_data(engine, data, table, update_columns=[]):
    """Upload the data to the SQL table.

    Args:
        engine (Engine obj): The connection to the database.
        data (list): A list of dict containing the column name as key and the value to upload as value.
        table (Table obj): The obj that represents the table to insert/update the data.
        update_columns (list): The list of columns to update on duplicated keys.
    """
    sql_insert = insert(table).values(data)                                                                                                             # create the insert query

    on_duplicate_keys_update = sql_insert.on_duplicate_key_update(                                                                                      # add the update part, if the data already exist in the table, it should update the old values (in the cvm the data can be modified)
        {col: sql_insert.inserted[col] for col in update_columns}
    )

    inserted = False
    for _ in range(5):                                                                                                                                  # if there is a connection error try at last for 5 times
        try:
            engine.execute(on_duplicate_keys_update)
            inserted = True
            print('Data uploaded!')
            break

        except db.exc.OperationalError as err:
            print(err.args)
            continue

    if not inserted:
        raise Exception('After 5 tries could not insert the data for the file.')                                                                        # if after 5 times it could not insert, rise a error


def upload_funds_quota(engine, table_name):
    """Upload the the funds quota and the liquid equity for each fund daily.

    Args:
        engine (Engine obj): The connection to the database.
        table_name (str): The table name to insert/update the data.
    """
    datatable_structure = [
        db.Column('date', db.Date(), nullable=False, default=None),
        db.Column('cnpj_fund', db.String(14), nullable=False, primary_key=True),
        db.Column('quota_date', db.Date(), nullable=False, primary_key=True),
        db.Column('quota', db.Float(32), default=None),
        db.Column('liquid_equity', db.Float(32), default=None)
    ]

    table = get_table(engine, datatable_structure, table_name)
    last_update_date, max_quota_date = get_last_update_date(engine, table)

    url = 'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/'

    parser_parametters = {
        'historical': {'html': request_get(f'{url}/HIST/'), 'pattern': r'inf_diario_fi_(\d{4}).zip'},
        'current': {'html': request_get(url), 'pattern': r'inf_diario_fi_(\d{6}).csv'}
    }

    url_files_list = get_url_files_list(parser_parametters, last_update_date, max_quota_date)

    rename_cols = {
        'CNPJ_FUNDO': 'cnpj_fund',
        'DT_COMPTC': 'quota_date',
        'VL_QUOTA': 'quota',
        'VL_PATRIM_LIQ':'liquid_equity'
    }

    csv_parse = {
        'sep': ';',
        'parse_dates': ['DT_COMPTC'],
        'usecols': list(rename_cols.keys())
    }

    df_replace = {
        'to_replace': {'CNPJ_FUNDO': '[\.\/\-]'},
        'value': '',
        'regex': True
    }

    update_columns = ['date', 'quota', 'liquid_equity']

    fill_na = {
        'quota': 0.0,
        'liquid_equity': 0.0
    }

    for df in get_data(url_files_list, rename_cols, csv_parse, df_replace):
        df['date'] = datetime.date.today()
        upload_data(engine, format_data(df, fill_na), table, update_columns)

def upload_funds_cadastre(engine, table_name):
    """Upload the funds cadastre information for each fund.

    Args:
        engine (Engine obj): The connection to the database.
        table_name (str): The table name to insert/update the data.
    """
    datatable_structure = [
        db.Column('cnpj_fund', db.String(14), nullable=False, primary_key=True),
        db.Column('fund_name', db.String(120), nullable=False),
        db.Column('situation', db.String(25), nullable=False),
        db.Column('class', db.String(30), default=None),
        db.Column('cnpj_adm', db.String(14), default=None),
        db.Column('adm', db.String(120), default=None),
        db.Column('cpf_cnpj_menager', db.String(14), default=None),
        db.Column('menager', db.String(120), default=None)
    ]

    table = get_table(engine, datatable_structure, table_name)

    rename_cols = {
        'CNPJ_FUNDO': 'cnpj_fund',
        'DENOM_SOCIAL': 'fund_name',
        'SIT':'situation',
        'CLASSE': 'class',
        'CNPJ_ADMIN':'cnpj_adm',
        'ADMIN':'adm',
        'CPF_CNPJ_GESTOR':'cpf_cnpj_menager',
        'GESTOR':'menager'
    }

    csv_parse = {
        'sep': ';',
        'encoding': 'latin-1',
        'usecols': list(rename_cols.keys()),
    }

    df_replace = {
        'to_replace': {'CNPJ_FUNDO': '[\.\/\-]', 'CNPJ_ADMIN': '[\.\/\-]', 'CPF_CNPJ_GESTOR': '[\.\/\-]'},
        'value': '',
        'regex': True
    }

    url = ['http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv']
    # TODO check the file last update date, and if it should update, check the data in the DB and in the file and just modify the rows that was modified
    update_columns = ['fund_name', 'situation', 'class', 'cnpj_adm', 'adm', 'cpf_cnpj_menager', 'menager']
    for df in get_data(url, rename_cols, csv_parse, df_replace):
        print(f'upload {table_name}')
        upload_data(engine, format_data(df), table, update_columns)

def main():
    engine = db.create_engine('mysql+pymysql://user:pass@host:port/db', pool_recycle=1)
    tables_name = {'table_cadastre': 'funds_cadastre', 'table_quota':'funds_quota'}

    upload_funds_cadastre(engine, tables_name['table_cadastre'])
    upload_funds_quota(engine, tables_name['table_quota'])


if __name__ == "__main__":
    main()