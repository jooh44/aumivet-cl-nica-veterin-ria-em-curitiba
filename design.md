# Aumivet — Design System

> Paleta expandida a partir das duas cores-âncora do logo, para um redesign que troca ilustração por fotografia.
>
> **Fonte:** Figma · [Aumivet / Paleta](https://www.figma.com/design/eIGmItv6LdatT0BOoMfKvj/Aumivet?node-id=7-8995) — node `7:8995`
> **Logo:** node `3:8476`

---

## 1. Famílias de cor

### 1.1 Aumi Pink

Cor de ação primária. Botões principais, links, destaques, estados ativos. O **500** é a cor original do logo.

| Token | Hex |
|---|---|
| `aumi-50` | `#FDEEF4` |
| `aumi-100` | `#FBD3E1` |
| `aumi-200` | `#F7A8C2` |
| `aumi-300` | `#F575A3` |
| `aumi-500` ★ | `#F24E88` |
| `aumi-600` | `#D43670` |
| `aumi-700` | `#A8295A` |
| `aumi-900` | `#6E1A3B` |

### 1.2 Vet Green

Cor de apoio e confiança. Sucesso, elementos de saúde, botões secundários. O **400** é a cor original do logo.

| Token | Hex |
|---|---|
| `vet-50` | `#EEF6E8` |
| `vet-100` | `#D3E8C4` |
| `vet-200` | `#AFD698` |
| `vet-400` ★ | `#81BD65` |
| `vet-500` | `#67A24B` |
| `vet-600` | `#4E8235` |
| `vet-700` | `#3A6326` |
| `vet-900` | `#234016` |

### 1.3 Neutros quentes

A base do sistema — ~70% da interface. Fundos, superfícies, texto, bordas. Levemente quentes para harmonizar com fotografia.

| Token | Hex |
|---|---|
| `neutral-50` | `#FAF8F5` |
| `neutral-100` | `#F0ECE6` |
| `neutral-200` | `#DDD6CC` |
| `neutral-300` | `#B5ADA0` |
| `neutral-500` | `#8A8175` |
| `neutral-700` | `#5C544A` |
| `neutral-900` | `#382F26` |

### 1.4 Apoio

Estende a harmonia. Pêssego e terracota são análogos quentes do rosa; o petróleo é um frio calmo que equilibra. Para gráficos, categorias e ilustrações remanescentes.

| Token | Hex |
|---|---|
| `peach-100` | `#FBE8DD` |
| `peach-400` | `#F2A878` |
| `terra-600` | `#C9603A` |
| `teal-100` | `#DDEBEA` |
| `teal-400` | `#5FA8A3` |
| `teal-700` | `#2C6B68` |

---

## 2. Aplicação

| Papel | Token |
|---|---|
| Fundo da página | `neutral-50` |
| Superfície (cards) | `#FFFFFF` |
| Linha / borda | `neutral-200` |
| Texto principal | `neutral-900` |
| Texto suave | `neutral-700` |
| Ação primária | `aumi-500` |
| Ação primária (hover) | `aumi-600` |
| Ação secundária | `vet-600` |
| Ação secundária (hover) | `vet-700` |

---

## 3. CSS — variáveis prontas

```css
:root {
  /* Aumi Pink */
  --aumi-50:  #FDEEF4;
  --aumi-100: #FBD3E1;
  --aumi-200: #F7A8C2;
  --aumi-300: #F575A3;
  --aumi-500: #F24E88;
  --aumi-600: #D43670;
  --aumi-700: #A8295A;
  --aumi-900: #6E1A3B;

  /* Vet Green */
  --vet-50:  #EEF6E8;
  --vet-100: #D3E8C4;
  --vet-200: #AFD698;
  --vet-400: #81BD65;
  --vet-500: #67A24B;
  --vet-600: #4E8235;
  --vet-700: #3A6326;
  --vet-900: #234016;

  /* Neutros quentes */
  --neutral-50:  #FAF8F5;
  --neutral-100: #F0ECE6;
  --neutral-200: #DDD6CC;
  --neutral-300: #B5ADA0;
  --neutral-500: #8A8175;
  --neutral-700: #5C544A;
  --neutral-900: #382F26;

  /* Apoio */
  --peach-100: #FBE8DD;
  --peach-400: #F2A878;
  --terra-600: #C9603A;
  --teal-100:  #DDEBEA;
  --teal-400:  #5FA8A3;
  --teal-700:  #2C6B68;

  /* Aplicação */
  --bg:        var(--neutral-50);
  --surface:   #FFFFFF;
  --text:      var(--neutral-900);
  --text-soft: var(--neutral-700);
  --line:      var(--neutral-200);
}
```

---

## 4. Tailwind — `theme.extend.colors`

```js
colors: {
  aumi:    { 50:'#FDEEF4',100:'#FBD3E1',200:'#F7A8C2',300:'#F575A3',500:'#F24E88',600:'#D43670',700:'#A8295A',900:'#6E1A3B' },
  vet:     { 50:'#EEF6E8',100:'#D3E8C4',200:'#AFD698',400:'#81BD65',500:'#67A24B',600:'#4E8235',700:'#3A6326',900:'#234016' },
  neutral: { 50:'#FAF8F5',100:'#F0ECE6',200:'#DDD6CC',300:'#B5ADA0',500:'#8A8175',700:'#5C544A',900:'#382F26' },
  peach:   { 100:'#FBE8DD',400:'#F2A878' },
  terra:   { 600:'#C9603A' },
  teal:    { 100:'#DDEBEA',400:'#5FA8A3',700:'#2C6B68' },
}
```

---

## 5. JSON — Design Tokens

```json
{
  "color": {
    "aumi":    { "50":"#FDEEF4","100":"#FBD3E1","200":"#F7A8C2","300":"#F575A3","500":"#F24E88","600":"#D43670","700":"#A8295A","900":"#6E1A3B" },
    "vet":     { "50":"#EEF6E8","100":"#D3E8C4","200":"#AFD698","400":"#81BD65","500":"#67A24B","600":"#4E8235","700":"#3A6326","900":"#234016" },
    "neutral": { "50":"#FAF8F5","100":"#F0ECE6","200":"#DDD6CC","300":"#B5ADA0","500":"#8A8175","700":"#5C544A","900":"#382F26" },
    "peach":   { "100":"#FBE8DD","400":"#F2A878" },
    "terra":   { "600":"#C9603A" },
    "teal":    { "100":"#DDEBEA","400":"#5FA8A3","700":"#2C6B68" }
  }
}
```

---

## 6. Notas de uso

- **★** marca as cores originais do logo (`aumi-500`, `vet-400`).
- Cores médias (300–500) de Aumi e Vet **não passam em contraste** para texto sobre branco. Para "cor de marca em texto", usar sempre **700 ou 900**.
- Sobre o `vet-400` (verde original), usar texto escuro (`vet-900`) — branco falha.
- Para botão primário, `aumi-500` com texto branco passa em AA.
- Os neutros são **quentes** intencionalmente: cinza azulado deixa fotografia de pele e pelagem doentia.
