import pandas as pd
from pathlib import Path
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

@task(retries=3)
def extract(dataset_url: str) -> pd.DataFrame:
    """Read NYC MVC data into pandas DataFrame."""
    return pd.read_csv(dataset_url)
    # return pd.read_csv('dataset.csv')

@task(log_prints=True)
def transform(data: pd.DataFrame) -> pd.DataFrame:
    """Basic transformation step. Merges columns CRASH DATE and CRASH TIME into a new column CRASH DATETIME."""
    data['CRASH DATETIME'] = data['CRASH DATE'] + ' ' + data['CRASH TIME']
    data['CRASH DATETIME'] = pd.to_datetime(data['CRASH DATETIME'], format='%m/%d/%Y %H:%M')
    data.drop(['CRASH DATE', 'CRASH TIME'], axis=1, inplace=True)
    return data

@task()
def write_local(data: pd.DataFrame, data_dir: str, dataset_filename='nyc_mvc') -> Path:
    """Write DataFrame as a parquet file."""
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    path = Path(f'{data_dir}/{dataset_filename}.parquet')
    data.to_parquet(path, compression='gzip')
    return path

@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS."""
    gcp_cloud_storage_bucket_block = GcsBucket.load("nyc-mvc-bucket")
    gcp_cloud_storage_bucket_block.upload_from_path(from_path=path, to_path=path)

@flow()
def nyc_mvc_etl(dataset_url: str = 'https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv') -> None:
    """Runs the NYC Motor Vehicle Collisions ETL flow. Extracts data from the web, transforms it and loads into GCS."""
    data = extract(dataset_url)
    data = transform(data)
    path = write_local(data, 'data')
    write_gcs(path)

if __name__ == '__main__':
    nyc_mvc_etl()