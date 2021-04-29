variable "project_name" {
  type        = string
  description = "Project name which will be used in tags and to create a resource group."
}

variable "public_subnets" {
  type        = list(string)
  description = "List of public subnets to launch the ENI"
}

variable "instance_ami" {
  type        = string
  description = "ec2 instance ami"
  default     = "ami-0742b4e673072066f"
}

variable "instance_type" {
  type        = string
  description = "ec2 instance type"
  default     = "t2.micro"
}

variable "vpc_id" {
  type        = string
  description = "VPC id for the instance to be launched in"
}

variable "key_name" {
  type        = string
  description = "Name of the key for the ec2 instance to be launched with"
}

