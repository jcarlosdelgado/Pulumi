# Despliegue de AWS EC2 (Frontend y Backend) con Pulumi en Python

Infraestructura como Codigo (IaC) para aprovisionar dos instancias EC2 ('frontend' y 'backend') en AWS utilizando Pulumi y Python, bajo una arquitectura modular limpia tipo Terraform.

---

## 1. Estructura del Proyecto

```text
Pulumi/
|-- infra/
|   |-- __init__.py
|   |-- config.py                 # Equivalente a 'variables.tf' (lectura de .env, nombres y tipos)
|   |-- security.py               # Equivalente a 'security.tf' (VPC, Subnets, KeyPair, Security Groups)
|   |-- compute.py                # Equivalente a 'compute.tf' / 'main.tf' (Instancias frontend y backend)
|   `-- outputs.py                # Equivalente a 'outputs.tf' (Exports de ambas instancias)
|-- scripts/
|   |-- user_data_frontend.sh     # Script de arranque para el servidor Frontend
|   `-- user_data_backend.sh      # Script de arranque para el servidor Backend
|-- .env                          # Variables locales con tus credenciales (ignorado por Git)
|-- .env.example                  # Plantilla de referencia para credenciales
|-- .gitignore                    # Reglas de exclusion de Git
|-- Pulumi.yaml                   # Metadatos del proyecto y configuracion de runtime
|-- Pulumi.dev.yaml               # Configuracion del stack dev
|-- requirements.txt              # Dependencias de Python
|-- __main__.py                   # Orquestador principal
|-- preview.sh                    # Script ejecutor para previsualizar
|-- up.sh                         # Script ejecutor para desplegar
|-- destroy.sh                    # Script ejecutor para destruir recursos
`-- README.md                     # Documentacion tecnica del proyecto
```

---

## 2. Arquitectura de las Instancias

### Instancia Frontend:
- Nombre: frontend
- Grupo de Seguridad: frontend-sg (Puertos 80 HTTP, 443 HTTPS y 22 SSH)
- Script de arranque: Instala servidor web Apache con pagina de bienvenida Frontend.
- Volumen: 20 GB gp3 con cifrado EBS habilitado.

### Instancia Backend:
- Nombre: backend
- Grupo de Seguridad: backend-sg (Puertos 80 HTTP, 8000/8080 API y 22 SSH)
- Script de arranque: Instala servidor web Apache con pagina de bienvenida Backend.
- Volumen: 20 GB gp3 con cifrado EBS habilitado.

---

## 3. Seguridad de Credenciales y GitHub

- El archivo .env esta completamente excluido por .gitignore y nunca sera rastreado por Git.
- No hay credenciales dentro del codigo Python.
- Los archivos de arranque estan desacoplados en scripts/ sin secretos.

---

## 4. Ejecucion en Git Bash

Desde tu terminal de Git Bash en la carpeta del proyecto:

### Paso 1: Previsualizar cambios
```bash
./preview.sh
```

### Paso 2: Desplegar en AWS
```bash
./up.sh
```
Confirma con 'yes' cuando te lo solicite. Al terminar, veras las IPs y URLs publicas de ambas instancias:
- frontend_url: http://<ip-frontend>
- backend_url: http://<ip-backend>

### Paso 3: Destruir los recursos
Cuando ya no uses las instancias, eliminalas para evitar cobros:
```bash
./destroy.sh
```
Confirma con 'yes'.

---

## 5. Como Subir a GitHub

```bash
git add .
git status
git commit -m "feat: arquitectura ec2 frontend y backend con pulumi python"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git push -u origin main
```
