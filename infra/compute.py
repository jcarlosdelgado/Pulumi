"""
Recursos de computo (equivalente a compute.tf / main.tf en Terraform).
Gestiona la creacion de las instancias EC2 'frontend' y 'backend' con volumenes cifrados.
"""

from pathlib import Path
from typing import Optional, Tuple
import pulumi_aws as aws
from infra.config import settings


def get_latest_amazon_linux_ami() -> aws.ec2.AwaitableGetAmiResult:
    """Busca dinamicamente la ultima AMI oficial de Amazon Linux 2023 x86_64."""
    return aws.ec2.get_ami(
        most_recent=True,
        owners=["137112412989"],
        filters=[
            aws.ec2.GetAmiFilterArgs(
                name="name",
                values=["al2023-ami-2023.*-kernel-6.1-x86_64"],
            ),
            aws.ec2.GetAmiFilterArgs(
                name="virtualization-type",
                values=["hvm"],
            ),
            aws.ec2.GetAmiFilterArgs(
                name="architecture",
                values=["x86_64"],
            ),
        ],
    )


def load_user_data(filename: str) -> str:
    """Carga el script de inicio especifico desde la carpeta scripts/."""
    script_path = Path(__file__).parent.parent / "scripts" / filename
    if script_path.exists():
        return script_path.read_text(encoding="utf-8")
    return ""


def create_compute_instances(
    subnet_id: str,
    frontend_sg_id: str,
    backend_sg_id: str,
    key_pair: Optional[aws.ec2.KeyPair] = None,
) -> Tuple[aws.ec2.Instance, aws.ec2.Instance]:
    """Crea las dos instancias EC2: frontend y backend."""
    ami = get_latest_amazon_linux_ami()
    key_name = key_pair.key_name if key_pair else None

    # 1. Instancia Frontend
    frontend = aws.ec2.Instance(
        settings.frontend_name,
        instance_type=settings.frontend_type,
        ami=ami.id,
        subnet_id=subnet_id,
        vpc_security_group_ids=[frontend_sg_id],
        key_name=key_name,
        user_data=load_user_data("user_data_frontend.sh"),
        root_block_device=aws.ec2.InstanceRootBlockDeviceArgs(
            volume_type="gp3",
            volume_size=20,
            encrypted=True,
            delete_on_termination=True,
        ),
        tags={
            "Name": settings.frontend_name,
            "Role": "frontend",
            "Environment": settings.environment,
            "ManagedBy": "Pulumi",
        },
    )

    # 2. Instancia Backend
    backend = aws.ec2.Instance(
        settings.backend_name,
        instance_type=settings.backend_type,
        ami=ami.id,
        subnet_id=subnet_id,
        vpc_security_group_ids=[backend_sg_id],
        key_name=key_name,
        user_data=load_user_data("user_data_backend.sh"),
        root_block_device=aws.ec2.InstanceRootBlockDeviceArgs(
            volume_type="gp3",
            volume_size=20,
            encrypted=True,
            delete_on_termination=True,
        ),
        tags={
            "Name": settings.backend_name,
            "Role": "backend",
            "Environment": settings.environment,
            "ManagedBy": "Pulumi",
        },
    )

    return frontend, backend
