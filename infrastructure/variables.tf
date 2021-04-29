variable "project_name" {
  type        = string
  description = "Project name which will be used in tags and to create a resource group."
}

variable "vpc_name" {
  type        = string
  description = "The name of the VPC"
}

variable "vpc_cidr_block" {
  type        = string
  description = "The CIDR block of the vpc"
}

variable "subnet_cidr_block" {
  type        = list(string)
  description = "Enter 4 subnet cidr blocks as a list Ex: [\"10.90.46.0/27\", \"10.90.46.32/27\"]"
}

variable "subnet_azs" {
  type        = list(string)
  description = "Enter 4 AZs where the subnet should be launched Ex: [\"us-east-1a\", \"us-east-1b\"]"
}

variable "subnet_type" {
  type        = list(string)
  description = "Enter whether subnet will be public,priv or data [\"public\", \"priv\",\"public\", \"priv\"]"
}

variable "key_name" {
  type        = string
  description = "Name of the key for the ec2 instance to be launched with"
}
