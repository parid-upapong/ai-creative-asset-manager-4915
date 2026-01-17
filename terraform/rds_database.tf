# PostgreSQL for Metadata and Analytics
resource "aws_db_subnet_group" "db_subnet" {
  name       = "creator-nexus-db-subnet"
  subnet_ids = aws_subnet.private[*].id
}

resource "aws_security_group" "rds_sg" {
  name   = "creator-nexus-rds-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [module.eks.node_security_group_id]
  }
}

resource "aws_db_instance" "metadata_db" {
  allocated_storage      = 50
  engine                 = "postgres"
  engine_version         = "15.3"
  instance_class         = "db.t3.large"
  db_name                = "creator_nexus_core"
  username               = "nexus_admin"
  password               = "REDACTED_USE_SECRETS_MANAGER"
  db_subnet_group_name   = aws_db_subnet_group.db_subnet.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  multi_az               = true
  storage_encrypted      = true
  skip_final_snapshot    = false
  final_snapshot_identifier = "creator-nexus-db-final-snap"
}