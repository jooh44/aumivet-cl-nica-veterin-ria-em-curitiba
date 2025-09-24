"""
Design Analysis Script for Aumivet Website
Uses Playwright to capture screenshots and analyze visual consistency
"""
import asyncio
from playwright.async_api import async_playwright
import os

async def analyze_aumivet_design():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Set viewport size for desktop analysis
        await page.set_viewport_size({"width": 1920, "height": 1080})

        try:
            # Navigate to the local site
            await page.goto("http://localhost:8000", wait_until="networkidle")

            # Wait for images and animations to load
            await page.wait_for_timeout(3000)

            # Create screenshots directory
            os.makedirs("screenshots", exist_ok=True)

            # Capture full page screenshot
            await page.screenshot(path="screenshots/full_page.png", full_page=True)
            print("Full page screenshot captured")

            # Capture individual sections
            sections = [
                ("hero-section", "Hero Section"),
                ("services", "Services Section"),
                ("specialized", "Specialized Services"),
                ("team", "Team Section"),
                ("testimonials", "Testimonials Section"),
                ("contato", "Contact Section")
            ]

            for section_id, section_name in sections:
                try:
                    element = await page.locator(f"#{section_id}").first
                    await element.screenshot(path=f"screenshots/{section_id}.png")
                    print(f"{section_name} screenshot captured")
                except Exception as e:
                    print(f"Could not capture {section_name}: {e}")

            # Capture mobile view
            await page.set_viewport_size({"width": 390, "height": 844})
            await page.screenshot(path="screenshots/mobile_full_page.png", full_page=True)
            print("Mobile full page screenshot captured")

        except Exception as e:
            print(f"Error analyzing website: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(analyze_aumivet_design())