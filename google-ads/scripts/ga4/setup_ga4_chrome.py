import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    # Caminho do perfil do Chrome no Linux
    user_data_dir = os.path.expanduser("~/.config/google-chrome")
    
    async with async_playwright() as p:
        # Tenta encontrar o executável do Chrome
        browser_path = "/usr/bin/google-chrome"
        if not os.path.exists(browser_path):
            browser_path = "/usr/bin/google-chrome-stable"

        print(f"🚀 Iniciando Chrome com perfil: {user_data_dir}")
        # Abrindo SEM headless para você poder logar se necessário
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            executable_path=browser_path,
            headless=False, # Modo com interface para interação
            args=["--no-sandbox", "--disable-extensions"]
        )
        
        page = await context.new_page()
        
        # 1. Ativar a API
        print("🔗 Indo para a página da API no Google Cloud...")
        await page.goto("https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com")
        
        print("\n--- AÇÃO REQUERIDA ---")
        print("Por favor, verifique a janela do Chrome que abriu.")
        print("1. Se não estiver logado, faça o login.")
        print("2. Se a API não estiver ativa, clique em 'Ativar'.")
        print("3. Quando terminar de ativar, me avise ou aguarde eu tentar prosseguir.")
        
        # Espera você interagir se precisar
        await asyncio.sleep(20) 
        
        # 2. Criar Conta de Serviço e Chave
        # Vamos tentar automatizar o restante se já estiver logado
        print("👤 Tentando acessar Service Accounts...")
        await page.goto("https://console.cloud.google.com/iam-admin/serviceaccounts")
        await asyncio.sleep(10)
        
        # Se você precisar fazer algo manual, pode fazer na janela aberta.
        # Vou manter a janela aberta por um tempo longo para você operar.
        print("Janela aberta. Você pode realizar o processo manualmente se preferir ou eu tento automatizar.")
        print("Vou aguardar 2 minutos com a janela aberta...")
        
        await asyncio.sleep(120)
        
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
