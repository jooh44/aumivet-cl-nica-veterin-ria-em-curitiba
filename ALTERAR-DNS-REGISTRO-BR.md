# 🔄 Alterar DNS do Registro.br - Passo a Passo

## 📋 Situação Atual
- **Domínio**: `aumivet.com.br`
- **DNS Atual**: Netlify
- **Objetivo**: Usar servidores DNS do Registro.br para gerenciar registros A

## ✅ Passo a Passo Completo

### 1. Acessar o Registro.br
- Vá para: https://registro.br/
- Faça login com sua conta

### 2. Selecionar o Domínio
- Na lista de domínios, clique em **`aumivet.com.br`**

### 3. Alterar Servidores DNS
- Clique em **"DNS"** no menu lateral
- Clique em **"Alterar servidores DNS"**
- Altere para os servidores DNS do Registro.br:

```
Servidor DNS 1: dns1.registro.br
Servidor DNS 2: dns2.registro.br
```

- Clique em **"Salvar"**

### 4. Aguardar Propagação
- ⏱️ **Tempo**: 2-24 horas (geralmente 1-2 horas)
- Verifique a propagação em: https://www.whatsmydns.net/#NS/aumivet.com.br

### 5. Após Propagação - Criar Registros A

Quando os servidores DNS estiverem propagados, você poderá criar os registros:

1. No Registro.br, vá em **"DNS"** → **"Gerenciar DNS"**
2. Adicione os seguintes registros:

#### Registro A para o domínio principal:
```
Tipo: A
Nome: @
Valor: 46.202.147.75
TTL: 3600
```

#### Registro A para www:
```
Tipo: A
Nome: www
Valor: 46.202.147.75
TTL: 3600
```

#### Registro A para subdomínio strapi (opcional):
```
Tipo: A
Nome: strapi
Valor: 46.202.147.75
TTL: 3600
```

## ⚠️ IMPORTANTE

1. **Tempo de Propagação**: Após alterar os servidores DNS, aguarde a propagação antes de criar os registros A
2. **Downtime**: Pode haver um período de indisponibilidade durante a mudança
3. **Netlify**: Se você estava usando Netlify, certifique-se de que não precisa mais dos serviços deles
4. **Verificação**: Use `nslookup aumivet.com.br` para verificar se está apontando corretamente

## 🔍 Verificar Configuração

Após criar os registros A, verifique:

```bash
# Verificar DNS
nslookup aumivet.com.br

# Deve retornar: 46.202.147.75
```

## 📝 Próximos Passos

Após o DNS estar configurado e propagado:

1. ✅ Verificar se o domínio aponta para o IP correto
2. ✅ Configurar SSL com Certbot:
   ```bash
   certbot --nginx -d aumivet.com.br -d www.aumivet.com.br
   ```
3. ✅ Testar acesso: https://aumivet.com.br

## 🆘 Troubleshooting

### Erro "Pesquisa recusada"
- Aguarde mais tempo para propagação
- Verifique se os servidores DNS foram alterados corretamente

### Domínio não resolve
- Verifique se os registros A foram criados corretamente
- Aguarde propagação completa (pode levar até 24h)

