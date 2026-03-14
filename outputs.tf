output "instance_public_ip" {
  description = "The public IP address of the EC2 instance"
  value       = aws_instance.app_server.public_ip
}

output "app_url" {
  description = "The URL to access your web application"
  value       = "http://${aws_instance.app_server.public_ip}"
}