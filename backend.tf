terraform {
  backend "s3" {
    bucket      = "pete-endgame-tf-state"
    key         = "tfstate/terraform.tfstate"
    region      = "eu-north-1"
    dynamodb_table = "pete-endgame-db"
    encrypt     = true
  }
}