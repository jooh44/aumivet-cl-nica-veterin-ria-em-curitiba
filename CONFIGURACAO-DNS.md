# 🌐 Configuração DNS - Aumivet.com.br

## 📋 Situação Atual

- **Domínio**: `aumivet.com.br` (registrado no Registro.br)
- **VPS**: Hostinger (IP: 46.202.147.75)
- **Subdomínio Strapi**: `strapi.digitaldog.pet` (já configurado)

## ✅ Opção 1: Alterar Servidores DNS no Registro.br (RECOMENDADO)

### Passo a Passo:

1. **Acesse o Registro.br**
   - Vá para: https://registro.br/
   - Faça login com sua conta

2. **Selecione o domínio `aumivet.com.br`**
   - Na lista de domínios, clique em `aumivet.com.br`

3. **Altere os Servidores DNS**
   - Vá em "DNS" → "Alterar servidores DNS"
   - **IMPORTANTE**: Primeiro, adicione o domínio no painel da Hostinger (hPanel)
   - Depois, use os servidores DNS da Hostinger:
     - `ns1.dns-parking.com`
     - `ns2.dns-parking.com`
     - (Ou os servidores específicos que a Hostinger fornecer)

4. **Configure os registros DNS na Hostinger**
   - Acesse o hPanel da Hostinger
   - Vá em "DNS" ou "Gerenciar DNS"
   - Adicione os seguintes registros:

### Registros DNS Necessários:

```
Tipo    Nome                    Valor              TTL
A       @                       46.202.147.75      3600
A       www                     46.202.147.75      3600
CNAME   strapi                  strapi.digitaldog.pet  3600
```

**OU** se quiser que o strapi também aponte para o IP:

```
Tipo    Nome                    Valor              TTL
A       @                       46.202.147.75      3600
A       www                     46.202.147.75      3600
A       strapi                  46.202.147.75      3600
```

## ✅ Opção 2: Manter DNS Atual e Criar Registros A (ALTERNATIVA)

Se você **NÃO quiser** alterar os servidores DNS, pode criar registros A diretamente no Registro.br:

1. **Acesse o Registro.br**
   - Vá em "DNS" → "Gerenciar DNS"

2. **Adicione os registros A**:
   ```
   Tipo: A
   Nome: @
   Valor: 46.202.147.75
   TTL: 3600
   
   Tipo: A
   Nome: www
   Valor: 46.202.147.75
   TTL: 3600
   ```

3. **Para o subdomínio strapi** (se quiser usar strapi.aumivet.com.br):
   ```
   Tipo: A
   Nome: strapi
   Valor: 46.202.147.75
   TTL: 3600
   ```

## ⏱️ Propagação DNS

- **Tempo estimado**: 2-24 horas
- **Verificar propagação**: https://www.whatsmydns.net/#A/aumivet.com.br

## 🔍 Verificar Configuração

Após configurar, verifique se está funcionando:

```bash
# Verificar DNS
nslookup aumivet.com.br
dig aumivet.com.br

# Verificar se aponta para o IP correto
curl -I http://aumivet.com.br
```

## ⚠️ IMPORTANTE

1. **Antes de alterar DNS**: Certifique-se de que os serviços estão rodando na VPS
2. **Backup**: Anote os servidores DNS atuais antes de alterar
3. **Propagação**: Pode levar até 24h para propagar completamente
4. **SSL**: Só configure SSL (Certbot) **DEPOIS** que o DNS estiver propagado

## 📝 Próximos Passos Após DNS Configurado

1. Aguardar propagação DNS (verificar com `nslookup`)
2. Configurar SSL com Certbot:
   ```bash
   certbot --nginx -d aumivet.com.br -d www.aumivet.com.br
   certbot --nginx -d strapi.digitaldog.pet
   ```
3. Testar acesso:
   - https://aumivet.com.br
   - https://strapi.digitaldog.pet

