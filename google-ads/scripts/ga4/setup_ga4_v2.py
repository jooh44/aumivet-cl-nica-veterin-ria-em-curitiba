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

        print("🚀 Abrindo Brave...")
        # Aumentamos o timeout para carregar o Console do Google que é pesado
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            executable_path=browser_path,
            headless=True,
            args=["--no-sandbox", "--window-size=1920,1080"]
        )
        context.set_default_timeout(60000)
        
        page = await context.new_page()
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        # 1. Ativar a API
        print("🔗 Acessando Library da API (Data API)...")
        try:
            await page.goto("https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com", wait_until="networkidle")
        except:
            print("⚠️ Timeout no carregamento, tentando prosseguir...")
        
        await asyncio.sleep(5)
        await page.screenshot(path=str(OUTPUT_DIR / "ga4_step1_library.png"))

        # Tenta clicar no botão Ativar
        enable_btn = page.get_by_role("button", name="Enable")
        if await enable_btn.is_visible():
            await enable_btn.click()
            print("✅ Botão 'Ativar' clicado.")
            await asyncio.sleep(10)
        else:
            print("ℹ️ API já ativa ou botão não visível.")

        # 2. Criar Conta de Serviço
        # Precisamos descobrir o projeto. Vamos tentar ir direto para a página de Service Accounts
        print("👤 Indo para Service Accounts...")
        await page.goto("https://console.cloud.google.com/iam-admin/serviceaccounts", wait_until="networkidle")
        await asyncio.sleep(5)
        await page.screenshot(path=str(OUTPUT_DIR / "ga4_step2_sa_list.png"))

        create_sa_btn = page.get_by_role("button", name="Create Service Account")
        if not await create_sa_btn.is_visible():
            create_sa_btn = page.get_by_label("Create Service Account")

        if await create_sa_btn.is_visible():
            await create_sa_btn.click()
            print("📝 Preenchendo formulário da Conta de Serviço...")
            await page.get_by_label("Service account name").fill("ga4-api-comissao")
            await asyncio.sleep(2)
            await page.get_by_role("button", name="Create and Continue").click()
            await asyncio.sleep(3)
            await page.get_by_role("button", name="Done").click()
            print("✅ Conta de serviço criada.")
        else:
            print("ℹ️ Botão de criar conta de serviço não encontrado.")

        # 3. Gerar Chave
        print("🔑 Gerando chave JSON...")
        # Recarrega para ver a lista atualizada
        await page.goto("https://console.cloud.google.com/iam-admin/serviceaccounts", wait_until="networkidle")
        await asyncio.sleep(5)
        
        sa_email_link = page.get_by_text("ga4-api-comissao@")
        if await sa_email_link.is_visible():
            await sa_email_link.first.click()
            await asyncio.sleep(5)
            await page.get_by_role("tab", name="Keys").click()
            await asyncio.sleep(2)
            await page.get_by_role("button", name="Add Key").click()
            await asyncio.sleep(1)
            await page.get_by_text("Create new key").click()
            await asyncio.sleep(1)
            
            async with page.expect_download() as download_info:
                await page.get_by_role("button", name="Create").click()
            
            download = await download_info.value
            output_path = DATA_DIR / "credentials-ga4.json"
            await download.save_as(str(output_path))
            print(f"🎉 ARQUIVO {output_path} GERADO!")
        else:
            print("❌ Não encontrei a conta ga4-api-comissao na lista.")

        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
