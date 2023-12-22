import pandas as pd
from io import BytesIO
import numpy as np

def conversor_vale_transporte_file(file):
     # Verifique se é um arquivo CSV
    if not file.filename.endswith('.csv'):
        raise ValueError("O arquivo não é um arquivo CSV válido.")
    # Script de coversão
    df = pd.read_csv(file)
    columns_drop = ['Cadastro','Valor Mult.','Numero','Qtd mensal','Descontos']
    correcao_colunas = df.drop(columns_drop, axis=1).rename(columns={'total a pedir':'Valor','CARTÃO':'Cartao'})
    correcao_colunas['CPF'] = correcao_colunas['CPF'].apply(lambda x: '{:.1f}'.format(x).rstrip('0').rstrip('.') if '.' in str(x) else str(x))
    correcao_colunas['CPF'] = correcao_colunas['CPF'].astype(str).str.zfill(11)
    correcao_cpf = correcao_colunas
    correcao_cpf['CPF'] = correcao_cpf['CPF'].str.replace(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', regex=True)
    correcao_cpf['Cartao'] = correcao_cpf['Cartao'].astype(str).str.rstrip('.0')
    correcao_cpf['Cartao'] = correcao_cpf['Cartao'].apply(lambda x: x.zfill(10))
    correcao_cpf['Cartao'] = correcao_cpf['Cartao'].str.replace(r'(\d{1})(\d{3})(\d{3})(\d{3})', r'\1.\2.\3.\4', regex=True)
    correcao_cartao = correcao_cpf
    correcao_cartao['Valor'] = correcao_cartao['Valor'].str.replace(',', '.')
    regex_aplicado = correcao_cartao
    df_corrigido = regex_aplicado.iloc[:-1]
    ORDEM_CORRETA = ['Nome','CPF','Cartao','Valor']
    df_corrigido = df_corrigido[ORDEM_CORRETA]

    # Salve o DataFrame convertido em XML em um buffer BytesIO
    output_buffer = BytesIO()
    df_corrigido.to_xml(output_buffer, index=False, root_name='DSImpCEValor', row_name='CE', encoding='utf-8')

    # Volte para o início do buffer
    output_buffer.seek(0)

    return output_buffer

def conversor_insalubridade(file):
  # Verifique se é um arquivo CSV
    #if not file.filename.endswith('.csv'):
    #    raise ValueError("O arquivo não é um arquivo CSV válido.")
    # Script de coversão

    df = pd.read_excel(file)
    todas_colunas = df.columns

    # Encontra a coluna que contém a parte variável
    coluna_variavel = [coluna for coluna in todas_colunas if 'HMCC - Aux/Téc Responsáveis Pacientes em Isolamento EXCEL' in coluna]

    # Verifica se a coluna foi encontrada
    if coluna_variavel:
        # Obtém o nome da coluna
        nome_coluna_variavel = coluna_variavel[0]

        # Renomeia a coluna para 'Matrícula'
        df = df.rename(columns={nome_coluna_variavel: 'Matrícula'})
        print(f"A coluna '{nome_coluna_variavel}' foi renomeada para 'Matrícula'.")
    else:
        print("Coluna não encontrada.")
    #Corrige as colunas do documento, deixando apenas as colunas necessárias.
    column_tofix = ['Unnamed: 1','Unnamed: 2']
    colunas_corrigidas= df.drop(column_tofix, axis=1).rename(columns={'Unnamed: 3':'Valor'})
    df_colunas_corrigidas = colunas_corrigidas
    #Corrige as Linhas do documento, removendo as linhas desnecessárias.
    fix_rows = df_colunas_corrigidas.drop(index=range(0,3))#.iloc[:-1]
    df_linhas_corrigidas = fix_rows
    #Adiciona os zeros a esquerda para deixar no padrão que a Senior pede.
    df_linhas_corrigidas['Matrícula'] = df_linhas_corrigidas['Matrícula'].astype(str).str.zfill(10)
    adiciona_zeros = df_linhas_corrigidas
    adiciona_zeros.round({'Valor': 2})
    #Retira os nomes das colunas para no arquivo final txt saia correto.
    adiciona_zeros.rename(columns={col: '' for col in adiciona_zeros.columns}, inplace=True)
    retira_nome_colunas = adiciona_zeros
    #Apenas para verificar se o DF está correto.
    df_final = retira_nome_colunas
    array_to_convert = df_final.to_numpy()
    # Salvar a matriz numpy em um arquivo temporário usando np.savetxt
    with BytesIO() as temp_file:
        np.savetxt(temp_file, array_to_convert, delimiter=';', fmt='%s')

        # Resetar o ponteiro do arquivo para o início
        temp_file.seek(0)

        # Ler o conteúdo do arquivo temporário usando BytesIO
        output_buffer = BytesIO(temp_file.read())

    return output_buffer    