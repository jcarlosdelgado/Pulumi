"""
Recursos de red y seguridad (equivalente a security.tf / network.tf en Terraform).
Gestiona la resolucion de VPC, Subnets, KeyPair y Grupos de Seguridad para frontend y backend.
"""

from typing import Optional, Tuple
import pulumi_aws as aws
from infra.config import settings


def get_network_context() -> Tuple[aws.ec2.AwaitableGetVpcResult, aws.ec2.AwaitableGetSubnetsResult]:
    """Obtiene la VPC por defecto y sus subredes asociadas."""
    vpc = aws.ec2.get_vpc(default=True)
    subnets = aws.ec2.get_subnets(
        filters=[aws.ec2.GetSubnetsFilterArgs(name="vpc-id", values=[vpc.id])]
    )
    return vpc, subnets


def create_key_pair() -> Optional[aws.ec2.KeyPair]:
    """Crea un KeyPair SSH en AWS si se proporciono una clave publica."""
    if not settings.ssh_public_key:
        return None
        
    return aws.ec2.KeyPair(
        "app-keypair",
        key_name="app-key",
        public_key=settings.ssh_public_key,
        tags={
            "Name": "app-key",
            "Environment": settings.environment,
            "ManagedBy": "Pulumi",
        },
    )


def create_frontend_security_group(vpc_id: str) -> aws.ec2.SecurityGroup:
    """Crea el Grupo de Seguridad para el Frontend (SSH, HTTP y HTTPS)."""
    return aws.ec2.SecurityGroup(
        f"{settings.frontend_name}-sg",
        description="Reglas de trafico para servidor Frontend",
        vpc_id=vpc_id,
        ingress=[
            aws.ec2.SecurityGroupIngressArgs(
                description="Acceso SSH",
                from_port=22,
                to_port=22,
                protocol="tcp",
                cidr_blocks=[settings.allowed_ssh_cidr],
            ),
            aws.ec2.SecurityGroupIngressArgs(
                description="Acceso HTTP web",
                from_port=80,
                to_port=80,
                protocol="tcp",
                cidr_blocks=["0.0.0.0/0"],
            ),
            aws.ec2.SecurityGroupIngressArgs(
                description="Acceso HTTPS web",
                from_port=443,
                to_port=443,
                protocol="tcp",
                cidr_blocks=["0.0.0.0/0"],
            ),
        ],
        egress=[
            aws.ec2.SecurityGroupEgressArgs(
                description="Permitir todo el trafico saliente",
                from_port=0,
                to_port=0,
                protocol="-1",
                cidr_blocks=["0.0.0.0/0"],
            )
        ],
        tags={
            "Name": f"{settings.frontend_name}-sg",
            "Environment": settings.environment,
            "ManagedBy": "Pulumi",
        },
    )


def create_backend_security_group(vpc_id: str) -> aws.ec2.SecurityGroup:
    """Crea el Grupo de Seguridad para el Backend (SSH, HTTP y puertos de API)."""
    return aws.ec2.SecurityGroup(
        f"{settings.backend_name}-sg",
        description="Reglas de trafico para servidor Backend / API",
        vpc_id=vpc_id,
        ingress=[
            aws.ec2.SecurityGroupIngressArgs(
                description="Acceso SSH",
                from_port=22,
                to_port=22,
                protocol="tcp",
                cidr_blocks=[settings.allowed_ssh_cidr],
            ),
            aws.ec2.SecurityGroupIngressArgs(
                description="Acceso HTTP",
                from_port=80,
                to_port=80,
                protocol="tcp",
                cidr_blocks=["0.0.0.0/0"],
            ),
            aws.ec2.SecurityGroupIngressArgs(
                description="Acceso API puerto 8000",
                from_port=8000,
                to_port=8000,
                protocol="tcp",
                cidr_blocks=["0.0.0.0/0"],
            ),
            aws.ec2.SecurityGroupIngressArgs(
                description="Acceso API puerto 8080",
                from_port=8080,
                to_port=8080,
                protocol="tcp",
                cidr_blocks=["0.0.0.0/0"],
            ),
        ],
        egress=[
            aws.ec2.SecurityGroupEgressArgs(
                description="Permitir todo el trafico saliente",
                from_port=0,
                to_port=0,
                protocol="-1",
                cidr_blocks=["0.0.0.0/0"],
            )
        ],
        tags={
            "Name": f"{settings.backend_name}-sg",
            "Environment": settings.environment,
            "ManagedBy": "Pulumi",
        },
    )
