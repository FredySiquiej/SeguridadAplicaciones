from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import hashlib
from urllib.parse import parse_qs, urlparse
import os
import modulo_que_no_existe


# Configuración de usuarios
USERS = {
    "admin": {
        "password": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",  # admin123
        "role": "admin",
        "name": "Administrador Principal"
    },
    "usuario": {
        "password": "ec1e5fb1598f356ab9226a023b6f47431e6b8b8a3c0e9c5d0a8e2c84c8c5c5b5",  # user123
        "role": "user",
        "name": "Usuario Regular"
    },
    "fredy": {
        "password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",  # 123
        "role": "superadmin",
        "name": "Fredy Super Admin"
    }
}

def hash_password(password):
    """Convierte la contraseña a hash SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

class LoginHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/dashboard':
            # Servir la página de dashboard
            self.serve_dashboard()
        elif parsed_path.path == '/':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        else:
            return SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        if self.path == '/api/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode())
            
            username = data.get('username', [''])[0]
            password = data.get('password', [''])[0]
            
            response = self.handle_login(username, password)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404)
    
    def handle_login(self, username, password):
        if not username or not password:
            return {"success": False, "message": "Usuario y contraseña requeridos"}
        
        if username not in USERS:
            return {"success": False, "message": "Usuario no encontrado"}
        
        hashed_password = hash_password(password)
        if USERS[username]['password'] != hashed_password:
            return {"success": False, "message": "Contraseña incorrecta"}
        
        return {
            "success": True,
            "message": "Login exitoso",
            "user": {
                "username": username,
                "role": USERS[username]['role'],
                "name": USERS[username]['name']
            },
            "redirect": "/dashboard"
        }
    
    def serve_dashboard(self):
        """Sirve la página de dashboard/welcome"""
        dashboard_html = '''
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dashboard - Sistema de Login</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    height: 100vh; 
                    display: flex; 
                    justify-content: center; 
                    align-items: center;
                }
                .dashboard-container { 
                    width: 100%; 
                    max-width: 600px; 
                    padding: 20px; 
                }
                .welcome-box { 
                    background: white; 
                    padding: 50px; 
                    border-radius: 20px; 
                    box-shadow: 0 25px 50px rgba(0,0,0,0.15);
                    text-align: center;
                }
                .welcome-icon { 
                    font-size: 80px; 
                    margin-bottom: 30px; 
                }
                .welcome-title { 
                    font-size: 36px; 
                    color: #333; 
                    margin-bottom: 20px;
                    font-weight: 300;
                }
                .user-name { 
                    font-size: 48px; 
                    color: #667eea; 
                    margin-bottom: 30px;
                    font-weight: 600;
                }
                .user-info { 
                    background: #f8f9fa; 
                    padding: 25px; 
                    border-radius: 15px; 
                    margin: 30px 0;
                    border-left: 5px solid #667eea;
                }
                .info-item { 
                    margin: 15px 0; 
                    font-size: 18px; 
                    color: #555;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                .info-label { 
                    font-weight: 600; 
                    color: #333;
                }
                .info-value { 
                    background: #667eea; 
                    color: white; 
                    padding: 5px 15px; 
                    border-radius: 20px;
                    font-size: 14px;
                }
                .logout-btn { 
                    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
                    color: white; 
                    border: none; 
                    padding: 15px 30px; 
                    border-radius: 10px; 
                    font-size: 16px; 
                    font-weight: 600;
                    cursor: pointer; 
                    transition: all 0.3s;
                    margin-top: 20px;
                }
                .logout-btn:hover { 
                    transform: translateY(-2px); 
                    box-shadow: 0 10px 20px rgba(255, 107, 107, 0.3);
                }
                .back-btn {
                    background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
                    color: white;
                    border: none;
                    padding: 12px 25px;
                    border-radius: 8px;
                    font-size: 14px;
                    cursor: pointer;
                    transition: all 0.3s;
                    margin-top: 15px;
                }
                .back-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 15px rgba(81, 207, 102, 0.3);
                }
                .welcome-message {
                    font-size: 18px;
                    color: #666;
                    line-height: 1.6;
                    margin-bottom: 30px;
                }
            </style>
        </head>
        <body>
            <div class="dashboard-container">
                <div class="welcome-box">
                    <div class="welcome-icon">🎉</div>
                    <h1 class="welcome-title">¡Bienvenido al Sistema!</h1>
                    
                    <div class="user-name" id="userName">Usuario</div>
                    
                    <p class="welcome-message">
                        Has ingresado exitosamente al sistema. 
                        Aquí puedes gestionar todas las funcionalidades disponibles 
                        según tu nivel de acceso.
                    </p>
                    
                    <div class="user-info">
                        <div class="info-item">
                            <span class="info-label">👤 Nombre de usuario:</span>
                            <span id="displayUsername">-</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">🎯 Rol en el sistema:</span>
                            <span class="info-value" id="userRole">-</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">🕐 Fecha de ingreso:</span>
                            <span id="loginTime">-</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">🔐 Estado:</span>
                            <span class="info-value" style="background: #51cf66;">Sesión Activa</span>
                        </div>
                    </div>
                    
                    <button class="logout-btn" onclick="logout()">🚪 Cerrar Sesión</button>
                    <br>
                    <button class="back-btn" onclick="goBack()">↩️ Volver al Login</button>
                </div>
            </div>

            <script>
                // Obtener parámetros de la URL
                const urlParams = new URLSearchParams(window.location.search);
                const username = urlParams.get('user');
                const role = urlParams.get('role');
                const name = urlParams.get('name');
                
                // Mostrar información del usuario
                if (name) {
                    document.getElementById('userName').textContent = name;
                    document.getElementById('displayUsername').textContent = username;
                    document.getElementById('userRole').textContent = role;
                } else {
                    // Si no hay parámetros, mostrar mensaje genérico
                    document.getElementById('userName').textContent = 'Invitado';
                }
                
                // Mostrar fecha y hora actual
                const now = new Date();
                document.getElementById('loginTime').textContent = 
                    now.toLocaleDateString('es-ES', { 
                        weekday: 'long', 
                        year: 'numeric', 
                        month: 'long', 
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                    });
                
                function logout() {
                    if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
                        window.location.href = '/';
                    }
                }
                
                function goBack() {
                    window.location.href = '/';
                }
                
                // Efecto de entrada
                document.addEventListener('DOMContentLoaded', function() {
                    const welcomeBox = document.querySelector('.welcome-box');
                    welcomeBox.style.opacity = '0';
                    welcomeBox.style.transform = 'translateY(30px)';
                    
                    setTimeout(() => {
                        welcomeBox.style.transition = 'all 0.8s ease';
                        welcomeBox.style.opacity = '1';
                        welcomeBox.style.transform = 'translateY(0)';
                    }, 100);
                });
            </script>
        </body>
        </html>
        '''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(dashboard_html.encode())

def create_html_file():
    """Crea el archivo HTML para el frontend"""
    html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh; 
            display: flex; 
            justify-content: center; 
            align-items: center;
        }
        .login-container { 
            width: 100%; 
            max-width: 450px; 
            padding: 20px; 
        }
        .login-box { 
            background: white; 
            padding: 40px; 
            border-radius: 15px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { 
            text-align: center; 
            margin-bottom: 30px; 
            color: #333; 
            font-size: 28px;
        }
        .input-group { 
            margin-bottom: 25px; 
        }
        label { 
            display: block; 
            margin-bottom: 8px; 
            color: #555; 
            font-weight: 600; 
            font-size: 14px;
        }
        input { 
            width: 100%; 
            padding: 15px; 
            border: 2px solid #e1e5e9; 
            border-radius: 8px; 
            font-size: 16px; 
            transition: all 0.3s;
        }
        input:focus { 
            outline: none; 
            border-color: #667eea; 
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        button { 
            width: 100%; 
            padding: 15px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            border: none; 
            border-radius: 8px; 
            font-size: 16px; 
            font-weight: 600;
            cursor: pointer; 
            transition: transform 0.2s;
            margin-top: 10px;
        }
        button:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        button:disabled { 
            background: #ccc; 
            cursor: not-allowed; 
            transform: none;
            box-shadow: none;
        }
        .message { 
            margin-top: 20px; 
            padding: 15px; 
            border-radius: 8px; 
            text-align: center; 
            font-weight: 600;
            font-size: 14px;
        }
        .success { 
            background: #d4edda; 
            color: #155724; 
            border: 1px solid #c3e6cb; 
        }
        .error { 
            background: #f8d7da; 
            color: #721c24; 
            border: 1px solid #f5c6cb; 
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-box">
            <h1>🔐 Iniciar Sesión</h1>
            <form id="loginForm">
                <div class="input-group">
                    <label for="username">👤 Usuario:</label>
                    <input type="text" id="username" name="username" required 
                           placeholder="Ingresa tu nombre de usuario">
                </div>
                
                <div class="input-group">
                    <label for="password">🔒 Contraseña:</label>
                    <input type="password" id="password" name="password" required 
                           placeholder="Ingresa tu contraseña">
                </div>
                
                <button type="submit" id="loginBtn">🚀 Ingresar al Sistema</button>
            </form>
            
            <div id="message" class="message"></div>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const loginBtn = document.getElementById('loginBtn');
            const messageDiv = document.getElementById('message');
            
            messageDiv.textContent = '';
            messageDiv.className = 'message';
            loginBtn.disabled = true;
            loginBtn.textContent = '⏳ Verificando...';
            
            try {
                const formData = new URLSearchParams();
                formData.append('username', username);
                formData.append('password', password);
                
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    messageDiv.textContent = '✅ Login exitoso! Redirigiendo...';
                    messageDiv.className = 'message success';
                    
                    // Redirigir a la página de dashboard después de 1 segundo
                    setTimeout(() => {
                        window.location.href = `/dashboard?user=${encodeURIComponent(data.user.username)}&role=${encodeURIComponent(data.user.role)}&name=${encodeURIComponent(data.user.name)}`;
                    }, 1000);
                    
                } else {
                    messageDiv.textContent = `❌ ${data.message}`;
                    messageDiv.className = 'message error';
                }
                
            } catch (error) {
                messageDiv.textContent = '❌ Error de conexión con el servidor';
                messageDiv.className = 'message error';
            } finally {
                loginBtn.disabled = false;
                loginBtn.textContent = '🚀 Ingresar al Sistema';
            }
        });
    </script>
</body>
</html>'''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    create_html_file()
    
    port = 8000
    server_address = ('', port)
    
    print("=" * 60)
    print("🚀 SISTEMA DE LOGIN CON DASHBOARD")
    print("=" * 60)
    print(f"📡 URL Login: http://localhost:{port}")
    print(f"📊 URL Dashboard: http://localhost:{port}/dashboard")
    print("=" * 60)
    print("👥 Usuarios: admin/admin123 | usuario/user123 | fredy/123")
    print("=" * 60)
    print("⏹️  Ctrl + C para detener")
    print("=" * 60)
    
    try:
        server = HTTPServer(server_address, LoginHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")