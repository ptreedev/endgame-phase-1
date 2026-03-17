variable "ssh_public_key" {
  description = "Public SSH key to register with AWS for EC2 access. Generate with ssh-keygen and store the private key in GitHub Secrets as SSH_PRIVATE_KEY."
  type        = string
}

variable "db_host" {
  type      = string
  sensitive = true
}

variable "db_username" {
  type      = string
  sensitive = true
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "db_name" {
  type      = string
  sensitive = true
}

variable "db_port" {
  type      = string
  sensitive = true
}

variable "cors_origin" {
  description = "The allowed CORS origin for the web application"
  type        = string
}