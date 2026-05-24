import asyncio
from playwright.async_api import async_playwright
import os
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "docs" / "evidencias" / "ga4"

async def main():
    user_data_dir = os.path.expanduser("~/.config/BraveSoftware/Brave-Browser")
    # Propriedade GA4 da RZVET (extraída do project-context.md)
    property_id = "294320922" 
    
    async with async_playwright() as p:
        browser_path = "/usr/bin/brave-browser" 
        if not os.path.exists(browser_path):
            browser_path = "/usr/bin/brave"

        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            executable_path=browser_path,
            headless=True,
            args=["--no-sandbox"]
        )
        
        page = await context.new_page()
        print(f"Acessando relatório de campanhas do GA4 para Property {property_id}...")
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # URL direta para o relatório de aquisição de tráfego por campanha (últimos 7 dias por padrão)
        # Vamos tentar carregar a página de relatórios
        url = f"https://analytics.google.com/analytics/web/#/p{property_id}/reports/explorer?params=_u..nav%3Dmrsu%26_r..explorerCard..seldim%3D%5B%22sessionCampaignName%22%5D"
        
        await page.goto(url)
        print("Aguardando carregamento dos dados (30s)...")
        await asyncio.sleep(30) # Analytics é pesado
        
        screenshot_path = OUTPUT_DIR / "ga4_campaign_report.png"
        await page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"Screenshot do relatório salvo em {screenshot_path}")
        
        # Tenta extrair dados da tabela via seletores simples se possível
        # Nota: O DOM do Analytics é complexo, isso é apenas uma tentativa inicial
        try:
            # Procura por linhas que pareçam conter 'google / cpc' ou nomes de campanhas
            rows = await page.query_selector_all("tr")
            print(f"Encontradas {len(rows)} linhas na tabela.")
            for i, row in enumerate(rows[:20]):
                text = await row.inner_text()
                if "google" in text.lower():
                    print(f"Linha {i}: {text.replace('\n', ' | ')}")
        except Exception as e:
            print(f"Erro ao extrair texto: {e}")

        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
