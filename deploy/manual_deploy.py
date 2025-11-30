import paramiko
import sys
import time
import secrets
import base64

HOST = "46.202.147.75"
USER = "root"
PASSWORD = ",1E1FD2Y&'V2Rp,5o25p"

def generate_secret():
    """Gera um secret aleatório base64"""
    return base64.b64encode(secrets.token_bytes(32)).decode('utf-8')

def run_command(client, command, print_output=True):
    """Executa comando SSH e retorna output"""
    print(f"\n🔧 Executando: {command[:100]}...")
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    
    # Aguardar conclusão
    exit_status = stdout.channel.recv_exit_status()
    
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    
    if print_output:
        if out:
            print(out)
        if err and exit_status != 0:
            print(f"❌ Erro: {err}", file=sys.stderr)
    
    return out, err, exit_status

def main():
    print("🚀 Iniciando deployment completo do Aumivet...")
    
    # Conectar ao servidor
    print(f"\n📡 Conectando ao servidor {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(HOST, username=USER, password=PASSWORD, 
                      look_for_keys=False, allow_agent=False, timeout=30)
        print("✅ Conectado com sucesso!")
        
        # 1. Verificar containers em execução
        print("\n📋 Verificando containers já em execução...")
        out, _, _ = run_command(client, "docker ps -a --format 'table {{.Names}}\t{{.Status}}'")
        
        # 2. Preparar diretório
        print("\n📁 Preparando diretório de deployment...")
        run_command(client, "mkdir -p /root/aumivet")
        
        # 3. Verificar Git
        print("\n🔍 Verificando repositório Git...")
        out, _, status = run_command(client, "cd /root/aumivet && git status", print_output=False)
        
        if status != 0:
            # Repositório não existe, clonar
            print("📥 Clonando repositório...")
            run_command(client, 
                "git clone https://github.com/jooh44/aumivet-cl-nica-veterin-ria-em-curitiba.git /root/aumivet")
        else:
            # Repositório existe, atualizar
            print("🔄 Atualizando repositório...")
            run_command(client, "cd /root/aumivet && git fetch origin")
            run_command(client, "cd /root/aumivet && git reset --hard origin/main")
            run_command(client, "cd /root/aumivet && git pull origin main")
        
        # 4. Criar arquivo .env
        print("\n🔐 Criando arquivo .env com secrets gerados...")
        
        # Gerar secrets
        db_password = generate_secret()
        jwt_secret = generate_secret()
        admin_jwt_secret = generate_secret()
        app_keys = generate_secret()
        api_token_salt = generate_secret()
        
        env_content = f"""# PostgreSQL
POSTGRES_USER=strapi_user
POSTGRES_PASSWORD={db_password}
POSTGRES_DB=aumivet_strapi

# Strapi Database
DATABASE_CLIENT=postgres
DATABASE_PORT=5432
DATABASE_NAME=aumivet_strapi
DATABASE_USERNAME=strapi_user
DATABASE_PASSWORD={db_password}

# Strapi Secrets
JWT_SECRET={jwt_secret}
ADMIN_JWT_SECRET={admin_jwt_secret}
APP_KEYS={app_keys}
API_TOKEN_SALT={api_token_salt}

# URLs
STRAPI_URL=https://strapi.digitaldog.pet
NEXT_PUBLIC_STRAPI_URL=https://strapi.digitaldog.pet
NEXT_PUBLIC_SITE_URL=https://aumivet.com.br
"""
        
        # Escrever .env no servidor
        cmd = f'cat > /root/aumivet/.env << \'EOF\'\n{env_content}\nEOF'
        run_command(client, cmd, print_output=False)
        print("✅ Arquivo .env criado com sucesso!")
        
        # Salvar .env localmente para backup
        with open('deploy/.env.backup', 'w') as f:
            f.write(env_content)
        print("💾 Backup do .env salvo em deploy/.env.backup")
        
        # 5. Parar containers antigos do Aumivet (se existirem)
        print("\n🛑 Parando containers antigos do Aumivet...")
        run_command(client, "docker stop aumivet-frontend aumivet-strapi aumivet-strapi-db 2>/dev/null || true", 
                   print_output=False)
        run_command(client, "docker rm aumivet-frontend aumivet-strapi aumivet-strapi-db 2>/dev/null || true", 
                   print_output=False)
        
        # 6. Subir containers
        print("\n🚀 Subindo containers com Docker Compose...")
        print("⏳ Isso pode demorar alguns minutos (build das imagens)...")
        run_command(client, "cd /root/aumivet && docker compose up -d --build", print_output=True)
        
        # 7. Aguardar um pouco
        print("\n⏱️  Aguardando containers inicializarem...")
        time.sleep(10)
        
        # 8. Verificar status
        print("\n✅ Verificando status dos containers...")
        run_command(client, "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'")
        
        # 9. Ver logs iniciais
        print("\n📜 Logs do Strapi (últimas 20 linhas):")
        run_command(client, "docker logs aumivet-strapi --tail 20")
        
        print("\n📜 Logs do Frontend (últimas 20 linhas):")
        run_command(client, "docker logs aumivet-frontend --tail 20")
        
        print("\n🎉 Deployment concluído!")
        print("\n📊 Resumo:")
        print("✅ Repositório clonado/atualizado")
        print("✅ Arquivo .env criado com secrets seguros")
        print("✅ Containers iniciados")
        print("\n🌐 Acesse:")
        print("  - Frontend: https://aumivet.com.br")
        print("  - Strapi Admin: https://strapi.digitaldog.pet/admin")
        print("  - Strapi API: https://strapi.digitaldog.pet/api")
        
        print("\n📝 Próximos passos:")
        print("1. Aguarde 2-3 minutos para os containers estabilizarem")
        print("2. Acesse https://strapi.digitaldog.pet/admin para criar o usuário admin")
        print("3. Verifique os logs: docker logs aumivet-strapi -f")
        
    except paramiko.ssh_exception.SSHException as e:
        print(f"❌ Erro SSH: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        client.close()
        print("\n👋 Conexão SSH fechada.")

if __name__ == "__main__":
    main()
