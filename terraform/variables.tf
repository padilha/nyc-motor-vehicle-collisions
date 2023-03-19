locals {
  data_lake_bucket = "nyc_mvc_data_lake"
}

variable "project" {
  description = "NYC Motor Vehicle Collisions project"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "europe-west6"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "nyc_mvc_data"
}
