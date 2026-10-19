#!/bin/bash
dnf update -y
dnf install -y httpd
systemctl start httpd
systemctl enable httpd

cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Backend - AWS EC2</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #0b132b; color: #f8fafc; text-align: center; padding: 60px 20px; }
        .card { background: #1c2541; border-radius: 12px; padding: 40px; max-width: 650px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border: 1px solid #3a506b; }
        h1 { color: #48cae4; margin-bottom: 10px; }
        p { color: #94a3b8; font-size: 16px; line-height: 1.6; }
        .badge { background: #0077b6; color: white; padding: 6px 16px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-block; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">Backend Instance</span>
        <h1>Servidor Backend Activo</h1>
        <p>API Backend aprovisionada con Pulumi y Python.</p>
    </div>
</body>
</html>
EOF
