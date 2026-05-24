import asyncio
from playwright.async_api import async_playwright
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "docs" / "evidencias" / "ga4"
DATA_DIR = PROJECT_ROOT / "data" / "credentials"

async def main():
    user_data_dir = os.path.expanduser("~/.config/BraveSoftware/Brave-Browser")
    
    async with async_playwright() as p:
        browser_path = "/usr/bin/brave-browser" 
        if not os.path.exists(browser_path): browser_path = "/usr/bin/brave"

        print("🚀 Iniciando Brave para configurar Google Cloud...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            executable_path=browser_path,
            headless=True,
            args=["--no-sandbox"]
        )
        
        page = await context.new_page()
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        # 1. Ativar a API
        print("🔗 Ativando Google Analytics Data API...")
        await page.goto("https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com")
        await asyncio.sleep(10)
        
        # Tenta clicar no botão "Ativar" se aparecer
        enable_button = await page.query_selector("button:has-text('Enable'), button:has-text('Ativar')")
        if enable_button:
            await enable_button.click()
            print("✅ Botão 'Ativar' clicado. Aguardando processamento...")
            await asyncio.sleep(15)
        else:
            print("ℹ️ API parece já estar ativa ou botão não encontrado.")

        # 2. Criar Conta de Serviço
        print("👤 Criando Conta de Serviço...")
        # Pega o ID do projeto atual da URL
        current_url = page.url
        project_id = current_url.split("project=")[1].split("&")[0] if "project=" in current_url else "seu-projeto"
        
        await page.goto(f"https://console.cloud.google.com/iam-admin/serviceaccounts?project={project_id}")
        await asyncio.sleep(10)
        
        create_button = await page.query_selector("button:has-text('Create Service Account'), button:has-text('Criar conta de serviço')")
        if create_button:
            await create_button.click()
            await asyncio.sleep(5)
            # Preenche o nome
            await page.fill("input[name='displayName']", "ga4-api-comissao")
            await page.press("input[name='displayName']", "Tab")
            await asyncio.sleep(2)
            # Clica em Criar
            create_done = await page.query_selector("button:has-text('Create and Continue'), button:has-text('Criar e continuar')")
            if create_done:
                await create_done.click()
                await asyncio.sleep(3)
                # Pula permissões (clica em Done)
                done_button = await page.query_selector("button:has-text('Done'), button:has-text('Concluir')")
                if done_button: await done_button.click()
            print("✅ Conta de serviço 'ga4-api-comissao' criada.")
        
        # 3. Gerar Chave JSON
        print("🔑 Gerando chave JSON...")
        await asyncio.sleep(5)
        # Tenta achar o link da conta recém criada
        sa_link = await page.query_selector("a:has-text('ga4-api-comissao')")
        if sa_link:
            await sa_link.click()
            await asyncio.sleep(5)
            await page.click("div[role='tab']:has-text('Keys'), div[role='tab']:has-text('Chaves')")
            await asyncio.sleep(3)
            await page.click("button:has-text('Add Key'), button:has-text('Adicionar chave')")
            await asyncio.sleep(2)
            await page.click("span:has-text('Create new key'), span:has-text('Criar nova chave')")
            await asyncio.sleep(2)
            
            # Aqui o navegador baixaria o arquivo. Em headless, precisamos capturar o evento de download.
            async with page.expect_download() as download_info:
                await page.click("button:has-text('Create'), button:has-text('Criar')")
            download = await download_info.value
            output_path = DATA_DIR / "credentials-ga4.json"
            await download.save_as(str(output_path))
            print(f"🎉 Arquivo {output_path} salvo com sucesso!")
        
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
