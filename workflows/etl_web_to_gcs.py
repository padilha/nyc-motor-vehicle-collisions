import pandas as pd
import math
from pathlib import Path
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

@task(retries=3)
def extract(dataset_url: str) -> pd.DataFrame:
    """Read NYC MVC data into pandas DataFrame."""
    return pd.read_csv(dataset_url)

@task(log_prints=True)
def transform(data: pd.DataFrame) -> pd.DataFrame:
    """Merges columns CRASH DATE and CRASH TIME into a new column CRASH DATETIME and transforms ZIP CODE column to int.
    """
    def transform_zipcode(zip_code):
        if isinstance(zip_code, str):
            zip_code = zip_code.strip()
            if zip_code:
                return int(zip_code)
            return -1
        if math.isnan(zip_code):
            return -1
        return int(zip_code)

    data['ZIP CODE'] = data['ZIP CODE'].apply(transform_zipcode)
    data['CRASH DATETIME'] = data['CRASH DATE'] + ' ' + data['CRASH TIME']
    data['CRASH DATETIME'] = pd.to_datetime(data['CRASH DATETIME'], format='%m/%d/%Y %H:%M')
    data.drop(['CRASH DATE', 'CRASH TIME'], axis=1, inplace=True)
    return data

@task()
def write_to_local(data: pd.DataFrame, data_dir: str = 'raw', dataset_filename: str = 'nyc_mvc') -> Path:
    """Write DataFrame as a parquet file."""
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    path = Path(f'{data_dir}/{dataset_filename}.parquet')
    data.to_parquet(path, compression='gzip')
    return path

@task()
def write_to_gcs(path: Path) -> None:
    """Upload local parquet file to GCS."""
    gcp_cloud_storage_bucket_block = GcsBucket.load("nyc-mvc-bucket")
    gcp_cloud_storage_bucket_block.upload_from_path(from_path=path, to_path=path)

@flow()
def nyc_mvc_etl(dataset_url: str = 'https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv') -> None:
    """Runs the NYC Motor Vehicle Collisions ETL flow. Extracts data from the web, transforms and loads it into GCS."""
    data = extract(dataset_url)
    data = transform(data)
    path = write_to_local(data)
    write_to_gcs(path)

if __name__ == '__main__':
    nyc_mvc_etl()