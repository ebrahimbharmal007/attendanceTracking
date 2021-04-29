project_name = "attendance"
vpc_name = "attendancevpc"
vpc_cidr_block = "10.18.0.0/16"
subnet_cidr_block = ["10.18.1.0/24", "10.18.2.0/24", "10.18.3.0/24", "10.18.4.0/24"]
subnet_azs = ["us-east-1a", "us-east-1a", "us-east-1b", "us-east-1b"]
subnet_type = ["public", "priv", "public", "priv"]
key_name = "attendance"