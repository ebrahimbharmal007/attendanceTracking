provider "aws" {
  region                  = "us-east-1"
  shared_credentials_file = "C:\\Users\\Ebrahim\\.aws"
  profile                 = "default"
}

resource "aws_resourcegroups_group" "project_resource_group" {
  name = "${var.project_name}_resources"

  resource_query {
    query = <<JSON
  {
    "ResourceTypeFilters": [
      "AWS::AllSupported"
    ],
    "TagFilters": [
      {
        "Key": "Project",
        "Values": ["${var.project_name}"]
      }
    ]
  }
  JSON
  }
}

module "vpc_setup" {
  source            = "C:\\Users\\Ebrahim\\Desktop\\Folders\\AttendanceTracking\\infrastructure\\modules\\vpc_setup"
  project_name      = var.project_name
  vpc_name          = var.vpc_name
  vpc_cidr_block    = var.vpc_cidr_block
  subnet_cidr_block = var.subnet_cidr_block
  subnet_azs        = var.subnet_azs
  subnet_type       = var.subnet_type
}

module "instance_setup" {
  source         = "C:\\Users\\Ebrahim\\Desktop\\Folders\\AttendanceTracking\\infrastructure\\modules\\instance_setup"
  project_name   = var.project_name
  public_subnets = module.vpc_setup.public_subnet_ids
  vpc_id         = module.vpc_setup.vpc_id
  key_name       = var.key_name
}

resource "aws_db_subnet_group" "private_db" {
  name       = "${var.vpc_name}_priv_subnetgroup"
  subnet_ids = module.vpc_setup.private_subnet_ids

  tags = {
    Name    = "${var.vpc_name}_priv_subnetgroup"
    Project = var.project_name
  }
}

resource "aws_db_instance" "attendance_db" {
  allocated_storage   = 10
  engine              = "mysql"
  instance_class      = "db.t2.micro"
  name                = "${lower(var.project_name)}db"
  username            = "admin"
  password            = "attendance"
  skip_final_snapshot = true
  depends_on = [
    aws_db_subnet_group.private_db
  ]
  db_subnet_group_name = aws_db_subnet_group.private_db.name

  tags = {
    Name    = "${var.project_name}-db"
    Project = var.project_name
  }
}
