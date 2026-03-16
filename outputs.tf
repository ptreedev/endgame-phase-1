output "static_public_ip" {
  description = "The permanent Elastic IP address of the EC2 instance"
  value       = aws_eip.app_eip.public_ip
}

output "app_url" {
  description = "The URL to access your web application"
  value       = "http://${aws_eip.app_eip.public_ip}"
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_id" {
  value = aws_subnet.public.id
}