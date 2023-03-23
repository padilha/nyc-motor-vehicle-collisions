locals {
  data_lake_bucket = "nyc_mvc_data_lake"
}

variable "project" {
  description = "NYC Motor Vehicle Collisions project"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default     = "us-central1"
  type        = string
}

variable "zone" {
  description = "Region for GCP instance."
  default     = "us-central1-a"
}

variable "instance_name" {
  default = "nyc-mvc-instance-terraform"
  type    = string
}

variable "prefect_api_key" {
  type = string
}

variable "prefect_workspace" {
  type = string
}

variable "dockerhub_user" {
  type = string
}

variable "dockerhub_passwd" {
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
