"""
Configuracion y variables del proyecto (equivalente a variables.tf en Terraform).
Define valores para las instancias frontend y backend.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import pulumi

# Cargar variables de entorno desde .env local si existe
ENV_FILE = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=ENV_FILE)

# Configurar passphrase por defecto para Pulumi local si no se definio
if "PULUMI_CONFIG_PASSPHRASE" not in os.environ:
    os.environ["PULUMI_CONFIG_PASSPHRASE"] = "dev"


@dataclass(frozen=True)
class AppConfig:
    """Contenedor de configuracion tipado e inmutable."""
    frontend_name: str
    backend_name: str
    frontend_type: str
    backend_type: str
    allowed_ssh_cidr: str
    ssh_public_key: Optional[str]
    environment: str


def load_config() -> AppConfig:
    """Carga y valida los parametros de configuracion."""
    cfg = pulumi.Config()
    
    return AppConfig(
        frontend_name=cfg.get("frontend_name") or "frontend",
        backend_name=cfg.get("backend_name") or "backend",
        frontend_type=cfg.get("frontend_type") or "t3.micro",
        backend_type=cfg.get("backend_type") or "t3.micro",
        allowed_ssh_cidr=cfg.get("allowed_ssh_cidr") or "0.0.0.0/0",
        ssh_public_key=cfg.get("ssh_public_key"),
        environment=pulumi.get_stack(),
    )


# Instancia global de configuracion lista para importar
settings = load_config()
