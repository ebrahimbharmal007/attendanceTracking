output "public_subnet_ids" {
  value = local.public_subnets
}

output "vpc_id" {
  value = aws_vpc.vpc.id
}

output "private_subnet_ids" {
  value = local.private_subnets
}

