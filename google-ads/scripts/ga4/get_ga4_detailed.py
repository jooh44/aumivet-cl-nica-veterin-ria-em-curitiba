import asyncio
from playwright.async_api import async_playwright
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "docs" / "evidencias" / "ga4"

async def main():
    user_data_dir = os.path.expanduser("~/.config/BraveSoftware/Brave-Browser")
    property_id = "294320922" 
    
    async with async_playwright() as p:
        browser_path = "/usr/bin/brave-browser" 
        if not os.path.exists(browser_path): browser_path = "/usr/bin/brave"

        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            executable_path=browser_path,
            headless=True,
            args=["--no-sandbox", "--window-size=1920,1080"]
        )
        
        page = await context.new_page()
        # Filtro: Últimos 7 dias, Dimensão: Campanha da sessão, Mídia: cpc
        url = f"https://analytics.google.com/analytics/web/#/p{property_id}/reports/explorer?params=_u..nav%3Dmrsu%26_r..explorerCard..seldim%3D%5B%22sessionCampaignName%22%5D"
        
        print("Navegando...")
        await page.goto(url)
        
        print("Aguardando carregamento profundo (45s)...")
        await asyncio.sleep(45)
        
        # Tirar um print da tela inteira para debug visual
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        screenshot_path = OUTPUT_DIR / "ga4_debug_full.png"
        await page.screenshot(path=str(screenshot_path), full_page=True)
        
        # Tenta pegar dados via avaliação de JS no contexto da página
        data = await page.evaluate("""() => {
            const results = [];
            // O Analytics usa muito Shadow DOM ou iframes, mas as tabelas costumam estar em divs específicas
            // Vamos procurar por elementos que contenham valores numéricos e nomes de campanhas
            const cells = Array.from(document.querySelectorAll('div[role="cell"], td'));
            return cells.map(c => c.innerText).filter(t => t.length > 0);
        }""")
        
        print("--- Dados Brutos Encontrados ---")
        print(data[:50]) # Mostra os primeiros 50 itens
        
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
