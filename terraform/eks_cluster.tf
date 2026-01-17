# Managed Kubernetes for AI Workers and Backend API
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "creator-nexus-cluster"
  cluster_version = "1.27"

  vpc_id     = aws_vpc.main.id
  subnet_ids = aws_subnet.private[*].id

  eks_managed_node_groups = {
    # Standard nodes for API and Frontend
    general = {
      min_size     = 2
      max_size     = 5
      desired_size = 2
      instance_types = ["t3.medium"]
    }
    # GPU Nodes for Computer Vision (CLIP/Tagging Engine)
    ai_workers = {
      min_size     = 1
      max_size     = 10
      desired_size = 1
      instance_types = ["g4dn.xlarge"] # NVIDIA T4 Tensor Core
      labels = {
        workload = "ai-inference"
      }
    }
  }
}