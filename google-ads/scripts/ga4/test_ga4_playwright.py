import asyncio
from playwright.async_api import async_playwright
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "docs" / "evidencias" / "ga4"

async def main():
    user_data_dir = os.path.expanduser("~/.config/BraveSoftware/Brave-Browser")
    # Tenta usar o perfil Default. Se o Brave estiver aberto, isso falhará.
    
    async with async_playwright() as p:
        print("Lançando Brave com perfil de usuário...")
        try:
            # Brave no Linux costuma estar em /usr/bin/brave-browser ou similar
            browser_path = "/usr/bin/brave-browser" 
            if not os.path.exists(browser_path):
                browser_path = "/usr/bin/brave"

            context = await p.chromium.launch_persistent_context(
                user_data_dir,
                executable_path=browser_path,
                headless=True, # Vamos tentar headless primeiro para extrair dados
                args=["--no-sandbox"]
            )
            
            page = await context.new_page()
            print("Acessando GA4...")
            # URL da propriedade GA4 (substitua pelo seu Property ID se souber, ou apenas a base)
            # Como não temos o ID, vamos para a home do Analytics
            await page.goto("https://analytics.google.com/analytics/web/")
            
            # Espera carregar para ver se a sessão está ativa
            await asyncio.sleep(10) 
            
            title = await page.title()
            print(f"Título da página: {title}")
            
            if "Google Analytics" in title:
                print("Sessão parece ativa!")
                # Tira um print para confirmar onde estamos
                OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
                screenshot_path = OUTPUT_DIR / "ga4_session_check.png"
                await page.screenshot(path=str(screenshot_path))
                print(f"Screenshot salvo em {screenshot_path}")
            else:
                print("Não parece estar logado no GA4. Título recebido:", title)
            
            await context.close()
        except Exception as e:
            print(f"Erro ao acessar perfil: {e}")

if __name__ == "__main__":
    asyncio.run(main())
