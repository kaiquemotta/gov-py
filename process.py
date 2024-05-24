import zipfile
import requests
import io
import pprint
from bs4 import BeautifulSoup
from db import ConexaoMongoDB
from fundo import FundoInvestimento

BASE_URL= 'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/'    
fundos = []
file_name_real =''
    
def download_and_extract_zip(zip_url):
    global file_name_real
    response = requests.get(zip_url)
    if response.status_code == 200:
        zip_content = io.BytesIO(response.content)
        extracted_files = {}
        with zipfile.ZipFile(zip_content, 'r') as zip_file:
            file_name_real = zip_file.namelist()
            print(f"Arquivos no zip: {file_name_real}")
            for file_name in file_name_real:
                print(file_name_real)
                with zip_file.open(file_name) as file:
                    file_content = file.read()
                    extracted_files[file_name] = file_content.decode('utf-8')           
        return extracted_files
    else:
        print(f"Falha ao baixar o arquivo. Código de status: {response.status_code}")
        return None
    
def transform_in_dic(data_string):
    valueString = data_string[file_name_real[0]]  
    lines = valueString.split('\n')
    # Extract header
    header = process_header(lines)
    data_dict = {}
    # Iterate over each line starting from the second (actual data)
    for line in lines[1:]:
        if line != '':
            line.strip()
            values = line.split(';')
            fund_id = values[1]  # Assuming CNPJ_FUNDO is the key
            fund_data = dict(zip(header[0:], values[0:]))  # Mapping header values to actual data
            if fund_id not in data_dict:
                data_dict[fund_id] = []
            new_data = process_row(fund_data)
            data_dict[fund_id].append(new_data)
    return data_dict    
    
def return_last_file(soup):
    links = soup.select('pre a')
    ultimo_link = links[-1]
    ultimo_link_texto =  ultimo_link.text
    return ultimo_link_texto

def save_file ():
    conexao = ConexaoMongoDB()
    for  obj in fundos:
        registro =  obj.to_dict()
        id_inserido = conexao.inserir_registro(registro)
        print("ID do documento inserido:", id_inserido)
        
    
def fill_object(records):
    for key, data in records.items():
        for  obj in data:
            fundo = FundoInvestimento(
            TP_FUNDO=obj['TP_FUNDO'],
            CNPJ_FUNDO=obj['CNPJ_FUNDO'],
            DT_COMPTC=obj['DT_COMPTC'],
            VL_TOTAL=obj['VL_TOTAL'],
            VL_QUOTA=float(obj['VL_QUOTA']),
            VL_PATRIM_LIQ=float(obj['VL_PATRIM_LIQ']),
            CAPTC_DIA=float(obj['CAPTC_DIA']),
            RESG_DIA=float(obj['RESG_DIA']),
            NR_COTST=float(obj['NR_COTST'])
            )
        fundos.append(fundo)
            
       
def process_header(lines):
    header = lines[0].split(';')
    nr_cotst = header[8]
    if nr_cotst is not None:
        nr_cotst = nr_cotst.strip()
        del header[8]
        header.append(nr_cotst)
    return header 

def process_row(row):
    value = row.get('NR_COTST')
    if value is not None:
        value = value.strip()
        row['NR_COTST'] = value
    return row 
    
def main():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        page_content = response.content
        soup = BeautifulSoup(page_content, 'html.parser')
        last_file = return_last_file(soup)
        if last_file:
            full_url = requests.compat.urljoin(BASE_URL, last_file)
            print(f"A URL completa é: {full_url}")
            arquivos_extraidos = download_and_extract_zip(full_url)
            dic = transform_in_dic(arquivos_extraidos)
            fill_object(dic)
            save_file()
            print('Processo encerrado!')
        else:
            print(f"Link com texto '{last_file}' não encontrado.")
    else:
        print(f"Falha ao recuperar a página. Código de status: {response.status_code}")
     
        
if __name__ == "__main__":
    main()        