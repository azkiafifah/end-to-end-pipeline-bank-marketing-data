variable "project" {
  description = "project id for this project"
  default = "firm-pentameter-363006"
}

variable "credentials" {
  description = "google_credentials.json"
  default = "google_credentials.json"
}

variable "region" {
  description = "Region for GCP resources"
  type        = string
  default     = "US"
}

variable "bq_dataset" {
  description = "BigQuery dataset"
  type        = string
  default     = "bank_marketing"
}