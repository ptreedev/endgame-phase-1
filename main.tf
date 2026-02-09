provider "aws" {
  region = "eu-north-1"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }
  owners = ["099720109477"]
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

resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "private_key" {
  content  = tls_private_key.ssh_key.private_key_pem
  filename = "./.ssh/terraform_rsa"
}

resource "local_file" "public_key" {
  content  = tls_private_key.ssh_key.public_key_openssh
  filename = "./.ssh/terraform_rsa.pub"
}

resource "aws_instance" "app_server" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.micro"
  subnet_id              = "subnet-ba3fc8d3"
  vpc_security_group_ids = ["sg-0c30518db572cf4f2"]
  key_name               = "terraform-key"
  user_data = templatefile("${path.module}/cloud-init.yaml.tmpl", {
    instance_name = "pete-endgame-ec2"
    DB_HOST = var.db_host
    DB_USERNAME = var.db_username
    DB_PASSWORD = var.db_password
    DB_NAME = var.db_name
    DB_PORT = var.db_port
  })
  tags = {
    Name = "pete-endgame-ec2"
  }
}