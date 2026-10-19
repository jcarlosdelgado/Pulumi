"""
Definicion de salidas del stack (equivalente a outputs.tf en Terraform).
Exporta los identificadores, IPs y URLs de frontend y backend.
"""

from typing import Optional
import pulumi
import pulumi_aws as aws


def register_outputs(
    frontend: aws.ec2.Instance,
    backend: aws.ec2.Instance,
    frontend_sg: aws.ec2.SecurityGroup,
    backend_sg: aws.ec2.SecurityGroup,
    key_pair: Optional[aws.ec2.KeyPair] = None,
) -> None:
    """Registra y exporta las salidas de ambas instancias."""
    # Salidas Frontend
    pulumi.export("frontend_id", frontend.id)
    pulumi.export("frontend_public_ip", frontend.public_ip)
    pulumi.export("frontend_public_dns", frontend.public_dns)
    pulumi.export("frontend_sg_id", frontend_sg.id)
    pulumi.export(
        "frontend_url",
        frontend.public_ip.apply(lambda ip: f"http://{ip}" if ip else "Sin IP publica"),
    )

    # Salidas Backend
    pulumi.export("backend_id", backend.id)
    pulumi.export("backend_public_ip", backend.public_ip)
    pulumi.export("backend_public_dns", backend.public_dns)
    pulumi.export("backend_sg_id", backend_sg.id)
    pulumi.export(
        "backend_url",
        backend.public_ip.apply(lambda ip: f"http://{ip}" if ip else "Sin IP publica"),
    )

    if key_pair:
        pulumi.export("key_pair_name", key_pair.key_name)
