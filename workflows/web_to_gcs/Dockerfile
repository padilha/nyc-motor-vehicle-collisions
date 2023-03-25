FROM prefecthq/prefect:2.7.7-python3.9

COPY requirements.txt .

RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir
RUN mkdir -p /opt/prefect/flows

COPY etl_web_to_gcs.py /opt/prefect/flows/etl_web_to_gcs.py