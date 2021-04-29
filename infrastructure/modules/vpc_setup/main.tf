terraform {
  required_version = ">=0.12"
}

resource "aws_vpc" "vpc" {
  cidr_block           = var.vpc_cidr_block
  instance_tenancy     = "default"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name    = var.vpc_name
    Project = var.project_name
  }
}

resource "aws_subnet" "subnets" {
  count             = 4
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = element(var.subnet_cidr_block, count.index)
  availability_zone = element(var.subnet_azs, count.index)
  tags = {
    Name    = "subnet_${count.index + 1}_${element(var.subnet_type, count.index)}"
    VPC     = var.vpc_name
    type    = element(var.subnet_type, count.index)
    Project = var.project_name
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name    = "${var.vpc_name}_igw"
    VPC     = var.vpc_name
    Project = var.project_name
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name    = "${var.vpc_name}_public_rt"
    VPC     = var.vpc_name
    Project = var.project_name
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name    = "${var.vpc_name}_private_rt"
    VPC     = var.vpc_name
    Project = var.project_name
  }
}

locals {
  public_subnets = [for subnet in aws_subnet.subnets : subnet.id if subnet.tags["type"] != "priv"]
}

locals {
  private_subnets = [for subnet in aws_subnet.subnets : subnet.id if subnet.tags["type"] != "public"]
}

resource "aws_route_table_association" "public_subnets" {
  count          = 2
  subnet_id      = element(local.public_subnets, count.index)
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private_subnets" {
  count          = 2
  subnet_id      = element(local.private_subnets, count.index)
  route_table_id = aws_route_table.private.id
}

