terraform {
  required_version = ">=0.12"
}

resource "aws_network_interface" "network_interface" {
  subnet_id = var.public_subnets[0]
  tags = {
    Name    = "${var.project_name}_eni"
    Project = var.project_name
  }
}

resource "aws_instance" "instance" {
  ami           = var.instance_ami
  instance_type = var.instance_type
  key_name      = var.key_name

  network_interface {
    network_interface_id = aws_network_interface.network_interface.id
    device_index         = 0
  }

  tags = {
    Name    = "${var.project_name}_instance"
    Project = var.project_name
  }

  volume_tags = {
    Name    = "${var.project_name}_storage"
    Project = var.project_name
  }

}

resource "aws_eip" "bar" {
  vpc      = true
  instance = aws_instance.instance.id
  tags = {
    Name    = "${aws_instance.instance.tags["Name"]}_eip"
    Project = var.project_name
  }
}
