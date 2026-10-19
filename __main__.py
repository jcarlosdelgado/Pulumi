"""
Punto de entrada principal para el despliegue con Pulumi en AWS.
Orquesta la creacion de la arquitectura con instancias 'frontend' y 'backend'.
"""

from infra.security import (
    get_network_context,
    create_key_pair,
    create_frontend_security_group,
    create_backend_security_group,
)
from infra.compute import create_compute_instances
from infra.outputs import register_outputs

# 1. Obtener contexto de red (VPC y Subnets)
vpc, subnets = get_network_context()

# 2. Clave SSH (opcional)
key_pair = create_key_pair()

# 3. Grupos de Seguridad dedicados para Frontend y Backend
frontend_sg = create_frontend_security_group(vpc_id=vpc.id)
backend_sg = create_backend_security_group(vpc_id=vpc.id)

# 4. Creacion de las instancias EC2: frontend y backend
frontend_instance, backend_instance = create_compute_instances(
    subnet_id=subnets.ids[0],
    frontend_sg_id=frontend_sg.id,
    backend_sg_id=backend_sg.id,
    key_pair=key_pair,
)

# 5. Exportar outputs finales de ambas instancias
register_outputs(
    frontend=frontend_instance,
    backend=backend_instance,
    frontend_sg=frontend_sg,
    backend_sg=backend_sg,
    key_pair=key_pair,
)
