terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.5.0"
    }
  }
  required_version = ">= 1.2"

  backend "s3" {
    bucket         = "pete-l-endgame-tf-state-1010"
    key            = "pl-endgame/terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "pete-l-endgame-terraform-lock"
  }
}

provider "aws" {
  region = "eu-west-2"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }
  owners = ["099720109477"]
}

# Register the public key with AWS — the private key never touches Terraform
# or the runner. It is stored in the GitHub repository secrets and used by the runner to connect to the EC2 instance.
resource "aws_key_pair" "deployer" {
  key_name   = "terraform-key"
  public_key = var.ssh_public_key
}

# The EC2 Server
resource "aws_instance" "app_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  key_name               = aws_key_pair.deployer.key_name

  user_data = templatefile("${path.module}/cloud-init.yaml.tmpl", {
    instance_name = "pete-endgame-ec2"
    DB_HOST       = var.db_host
    DB_USERNAME   = var.db_username
    DB_PASSWORD   = var.db_password
    DB_NAME       = var.db_name
    DB_PORT       = var.db_port
    CORS_ORIGIN   = var.cors_origin
    SECRET_KEY    = var.secret_key
  })

  tags = {
    Name = "pete-endgame-ec2"
  }

  lifecycle {
    ignore_changes = [
      ami,
      user_data
    ]
  }
}

# Allocate a static Elastic IP and attach it to the EC2 instance
resource "aws_eip" "app_eip" {
  instance = aws_instance.app_server.id
  domain   = "vpc"

  tags = {
    Name = "endgame-static-ip"
  }
}