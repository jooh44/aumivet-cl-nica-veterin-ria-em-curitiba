"""
Importa catálogo da Tray (produção) para o DataCrazy CRM > Produtos.
Campos mapeados: name, id_sku, price, image, integration_slug="tray"
Produtos sem SKU usam "tray-{id}" como id_sku.
Skipa produtos já existentes (mesmo id_sku).
"""

import os, sys, time, json
import requests
from pathlib import Path

# --- credenciais ---
ROOT = Path(__file__).parent.parent.parent.parent
env_tray = ROOT / ".env.tray"
env_global = ROOT / ".env"


def load_env(path):
    env = {}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip("'\"")
    return env


tray = load_env(env_tray)
glob = load_env(env_global)

TRAY_HOST = tray["TRAY_API_ADDRESS"]
TRAY_TOKEN = tray["TRAY_ACCESS_TOKEN"]
DC_BASE = glob["DATACRAZY_API_BASE_URL"]
DC_TOKEN = glob["DATACRAZY_API_TOKEN"]

TRAY_HEADERS = {"Authorization": f"Token {TRAY_TOKEN}"}
DC_HEADERS = {"Authorization": f"Bearer {DC_TOKEN}", "Content-Type": "application/json"}


# --- carregar produtos já existentes no DataCrazy (paginado) ---
def fetch_existing_dc_skus():
    existing = {}
    skip = 0
    while True:
        r = requests.get(f"{DC_BASE}/products", headers=DC_HEADERS, params={"skip": skip}, timeout=15)
        r.raise_for_status()
        data = r.json()
        batch = data.get("data", [])
        for p in batch:
            existing[p["id_sku"]] = p["id"]
        if len(batch) < 100:
            break
        skip += 100
        time.sleep(0.3)
    return existing


# --- paginar produtos da Tray ---
def fetch_tray_products():
    products = []
    page = 1
    while True:
        r = requests.get(
            f"{TRAY_HOST}/products",
            headers=TRAY_HEADERS,
            params={"limit": 50, "page": page},
            timeout=20,
        )
        if r.status_code == 401:
            print("ERRO: token Tray expirou — rode tray_auth_check.py para renovar")
            sys.exit(1)
        r.raise_for_status()
        data = r.json()
        batch = data.get("Products", [])
        if not batch:
            break
        products.extend(p["Product"] for p in batch)
        total = data.get("paging", {}).get("total")
        print(f"  página {page}: {len(batch)} produtos (total acumulado: {len(products)}/{total})")
        if total and len(products) >= int(total):
            break
        page += 1
        time.sleep(0.3)
    return products


# --- extrair imagem principal ---
def first_image(product):
    imgs = product.get("ProductImage", [])
    if not imgs:
        return ""
    pi = imgs[0].get("ProductImage", {})
    return pi.get("https", pi.get("http", ""))


# --- criar produto no DataCrazy ---
def create_dc_product(p):
    sku = (p.get("model") or "").strip() or f"tray-{p['id']}"
    name = (p.get("name") or "").strip()
    try:
        price = float(p.get("price") or 0)
    except (ValueError, TypeError):
        price = 0.0
    img = first_image(p)

    payload = {
        "name": name,
        "id_sku": sku,
        "price": price,
        "image": img,
        "integration_slug": "tray",
    }
    r = requests.post(f"{DC_BASE}/products", headers=DC_HEADERS, json=payload, timeout=15)
    r.raise_for_status()
    return r.json()


# --- main ---
def main():
    print("=== Importação Tray → DataCrazy ===\n")

    print("Carregando produtos já existentes no DataCrazy...")
    existing = fetch_existing_dc_skus()
    print(f"  {len(existing)} produtos já cadastrados\n")

    print("Buscando catálogo da Tray (produção)...")
    products = fetch_tray_products()
    print(f"\n{len(products)} produtos recuperados da Tray\n")

    created = 0
    skipped = 0
    errors = []

    for i, p in enumerate(products, 1):
        sku = (p.get("model") or "").strip() or f"tray-{p['id']}"
        name = (p.get("name") or "")[:60]

        if sku in existing:
            print(f"[{i:3}/{len(products)}] SKIP  {sku!r:30} {name}")
            skipped += 1
            continue

        try:
            result = create_dc_product(p)
            print(f"[{i:3}/{len(products)}] OK    {sku!r:30} {name}")
            created += 1
            time.sleep(0.8)
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 429:
                wait = 10
                print(f"[{i:3}/{len(products)}] 429   aguardando {wait}s...")
                time.sleep(wait)
                try:
                    result = create_dc_product(p)
                    print(f"[{i:3}/{len(products)}] OK    {sku!r:30} {name} (retry)")
                    created += 1
                    time.sleep(0.8)
                except Exception as e2:
                    print(f"[{i:3}/{len(products)}] ERRO  {sku!r:30} {name} → {e2}")
                    errors.append({"sku": sku, "name": name, "error": str(e2)})
            else:
                print(f"[{i:3}/{len(products)}] ERRO  {sku!r:30} {name} → {e}")
                errors.append({"sku": sku, "name": name, "error": str(e)})
        except Exception as e:
            print(f"[{i:3}/{len(products)}] ERRO  {sku!r:30} {name} → {e}")
            errors.append({"sku": sku, "name": name, "error": str(e)})

    print(f"\n=== Resultado ===")
    print(f"  Criados : {created}")
    print(f"  Skipped : {skipped}")
    print(f"  Erros   : {len(errors)}")

    if errors:
        out = Path(__file__).parent / "import_errors.json"
        out.write_text(json.dumps(errors, ensure_ascii=False, indent=2))
        print(f"  Erros salvos em: {out}")


if __name__ == "__main__":
    main()
