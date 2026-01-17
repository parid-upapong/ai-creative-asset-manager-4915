# CreatorNexus AI: Security Hardening Architecture

## 1. Network Security (Perimeter Defense)
*   **VPC Isolation:** All compute (EKS) and databases (RDS) reside in private subnets with no direct internet access.
*   **NAT Gateway:** Outbound traffic for patching and model downloading is routed through managed NAT Gateways.
*   **WAF (Web Application Firewall):** AWS WAF is deployed in front of the CloudFront distribution/Load Balancer to mitigate SQLi, XSS, and DDoS attacks.

## 2. Data Protection (Encryption)
*   **At Rest:** 
    *   S3 assets are encrypted using AWS KMS with Customer Managed Keys (CMK).
    *   RDS instances use AES-256 encryption for underlying EBS volumes.
*   **In Transit:** 
    *   Mandatory TLS 1.2+ for all API communications.
    *   Internal traffic between microservices uses Kubernetes Network Policies to restrict lateral movement.

## 3. Identity & Access Management (IAM)
*   **Least Privilege:** Roles are scoped specifically to the service (e.g., the `cv_engine` can only read from the `uploads/` prefix and write to `processed/`).
*   **IRSA (IAM Roles for Service Accounts):** EKS pods use IRSA to securely associate AWS IAM roles with Kubernetes service accounts, eliminating the need for long-lived secret keys inside containers.

## 4. Monitoring & Governance
*   **GuardDuty:** Enabled for intelligent threat detection on VPC flow logs and CloudTrail.
*   **AWS Shield:** Standard DDoS protection enabled by default; Advanced for Production.
*   **CloudWatch Logs:** All AI processing logs and API access logs are centralized with 90-day retention for auditability.