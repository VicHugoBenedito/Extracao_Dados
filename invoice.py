import requests

user = "vitor.benedito"
password = "g&4A2t6d73!6"
url = "https://api.hinova.com.br/api/sga/v2/usuario/autenticar"

header = {"Content-Type": "application/json",
          "Authorization": f"Bearer {'4ac5d214c1b0b67cd8715ba5ee15488a65da3f580f0736e7ddb5413fbf5ff30cf247ad769c038a3b0b718afeb73f191f24ec7ec7caa552e8abefd9ffcf0272aac9102168a7d571fbbdbaa32b08b64b0249c0d0045903b2bb1b8f8d8dce584fea'}"
          
          }

data = {
    "usuario": user,
    "senha": password
}

response = requests.post(url, headers=header, json=data)

if response.status_code == 200:
    token_acess = response.json()["token_usuario"]
    
    url_invoice = "https://api.hinova.com.br/api/sga/v2/listar/boleto"
    
    data_invoice = {
        "data_vencimento_original_inicial":"10/06/2024",
        "data_vencimento_original_final":"30/06/2024",
        "inicio_paginacao": 0,
        "quantidade_pagina":5000
    }
    
    header = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {token_acess}"
    }
    
    num_downloads = 0 
    ticket = []
    
    while True:
        response_invoice = requests.post(url_invoice, headers=header, json=data_invoice)
        
        if response_invoice.status_code == 200:
            
            ticket_page = response_invoice.json()
            ticket.extend(ticket_page)
            num_downloads += 1
            
            print(f"Download page {num_downloads} sucessfully conclued")
            
            if len(ticket_page) < 5000:
                print("Json downloaded sucessfully")
                break
            else:
                data_invoice["inicio_paginacao"] += 1
        else:
            print(f"Error{response_invoice.status_code}")
            print(response_invoice.text)        
            break

else:
    print(f"Error{response.status_code}")
    print(f'Error{response.text}')
    
import pandas as pd

df = pd.DataFrame(ticket)           

df["data_emissao"] = df["data_emissao"].apply(lambda x: x.split("T")[0] if pd.notnull(x) else '1901-01-01')
df["data_vencimento_original"] = df["data_vencimento_original"].apply(lambda x: x.split("T")[0] if pd.notnull(x) else '1901-01-01')
df["data_vencimento"] = df["data_vencimento"].apply(lambda x: x.split("T")[0] if pd.notnull(x) else '1901-01-01')
df["data_pagamento"] = df["data_pagamento"].apply(lambda x: x.split("T")[0] if pd.notnull(x) else '')

clear_columns = ["nome_associado","cpf_associado","codigo_situacao_associado",
                    "descricao_situacao_associado","nome_regional_associado",
                    "codigo_boleto","nome_regional_boleto","mes_referente",
                    "data_credito_banco","codigo_forma_pagamento","codigo_tipo_boleto",
                    "codigo_conta","codigo_banco","nome_banco","agencia","conta","beneficiario"]
df.drop(clear_columns, axis=1, inplace=True)
df = df.rename(columns=lambda x: x.upper())

df['VEICULO'] = df['VEICULO'].apply(lambda x: '/'.join(x))

import numpy as np

df = df.replace({np.nan: None})
collumns_order = [
"CODIGO_ASSOCIADO", "CODIGO_REGIONAL_ASSOCIADO", "NOSSO_NUMERO", "CODIGO_SITUACAO_BOLETO", 
"DESCRICAO_SITUACAO_BOLETO", "CODIGO_REGIONAL", "DATA_EMISSAO", "DATA_VENCIMENTO_ORIGINAL", 
"DATA_VENCIMENTO", "VALOR_BOLETO", "DATA_PAGAMENTO", "VALOR_PAGAMENTO", "DESCRICAO_FORMA_PAGAMENTO", 
"PARCELA_PAGA", "QTDE_PARCELA", "DESCRICAO_TIPO_COBRANCA_RECORRENTE", "DESCRICAO_TIPO_BOLETO", 
"DESCRICAO_TIPO_BAIXA_BOLETO", "VEICULO", "PAGO"]

df = df[collumns_order] 

df.to_csv("/mnt/c/Users/Vitor/Desktop/analise.csv", index=False)
    