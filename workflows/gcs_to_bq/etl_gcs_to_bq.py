import pandas as pd
import re
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(retries=3)
def extract(gcs_path : str = 'raw/nyc_mvc.parquet') -> pd.DataFrame:
    """Downloads NYC MVC data from GCS."""
    gcs_block = GcsBucket.load("nyc-mvc-bucket")
    gcs_block.get_directory(from_path=gcs_path, local_path='./')
    return pd.read_parquet(gcs_path)

@task()
def transform(data: pd.DataFrame) -> pd.DataFrame:
    """Transforms string columns by stripping leading and trailing whitespaces, replacing multiple spaces with a single space
    and bringing all column names to lowercase."""
    def transform_value(value):
        if isinstance(value, str):
            value = value.strip().lower()
            value = re.sub('\s+', ' ', value)
        return value
    
    columns_to_transform = [
        'BOROUGH',
        'ON STREET NAME',
        'CROSS STREET NAME',
        'OFF STREET NAME',
        'CONTRIBUTING FACTOR VEHICLE 1',
        'CONTRIBUTING FACTOR VEHICLE 2',
        'CONTRIBUTING FACTOR VEHICLE 3',
        'CONTRIBUTING FACTOR VEHICLE 4',
        'CONTRIBUTING FACTOR VEHICLE 5',
        'VEHICLE TYPE CODE 1',
        'VEHICLE TYPE CODE 2',
        'VEHICLE TYPE CODE 3',
        'VEHICLE TYPE CODE 4',
        'VEHICLE TYPE CODE 5',
    ]
    
    for c in columns_to_transform:
        data[c] = data[c].apply(transform_value)
    
    data.columns = [re.sub('\s+', '_', c.strip().lower()) for c in data.columns]
    
    return data

@task()
def write_to_bigquery(
    data: pd.DataFrame,
    destination_table: str = 'nyc_mvc_data.crashes',
    project_id: str = 'leafy-momentum-381114',
    chunksize: int = 300_000
) -> None:
    """Write DataFrame to BigQuery"""
    gcp_credentials_block = GcpCredentials.load('nyc-mvc-credentials')
    data.to_gbq(
        destination_table=destination_table,
        project_id=project_id,
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=chunksize,
        if_exists='replace'
    )

@flow()
def etl_gcs_to_bq():
    """Main ETL flow to extract data from GCS, transform and load it into BigQuery."""
    data = extract()
    data = transform(data)
    write_to_bigquery(data)

if __name__ == '__main__':
    etl_gcs_to_bq()