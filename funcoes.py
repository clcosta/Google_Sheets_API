def arrumar_cpf(numeros):
    """
    Padrinizar os CPFs da minha Tabela, já que ela recebe informações diretas de um Formulário pode ter erros dos Clientes.

    Args:
    numeros : Cpfs > Pensado para ser usado em um For dentro de uma tabela.

    Return : Retorna o CPF sem espaços ou quaisquer caracter que não seja numeros. | Considerando alertar erros de digitação se o CPF não tiver 11 Numeros(padrão CPF Brasileiro) o programa vai retonar o CPF tratado com um '*' antes do número.
    """
    if type(numeros) != str:
        numeros = str(numeros)
    if type(numeros) == str:
        try:
            if '.' in numeros or '-' in numeros or ' ' in numeros or ',' in numeros or 'R$' in numeros or '$' in numeros or 'cpf' in numeros or 'CPF' in numeros or ';' in numeros or ':' in numeros:
                if '.' in numeros:
                    numeros = numeros.replace('.', '')
                if '-' in numeros:
                    numeros = numeros.replace('-', '')
                if ' ' in numeros:
                    numeros = numeros.replace(' ', '')
                if ',' in numeros:
                    numeros = numeros.replace(',', '')
                if 'R$' in numeros:
                    numeros = numeros.replace('R$', '')
                if '$' in numeros:
                    numeros = numeros.replace('$', '')
                if 'cpf' in numeros:
                    numeros = numeros.replace('cpf','')
                if 'CPF' in numeros:
                    numeros = numeros.replace('CPF','')
                if ';' in numeros:
                    numeros = numeros.replace(';','')
                if ':' in numeros:
                    numeros = numeros.replace(':','')
        except:
            return '* ' + numeros
    if len(numeros) == 11:
        return numeros
    else:
        return '* ' + numeros

def padronizar_texto(texto):
    """
    Padronizar Textos > Pensado para ser utiliado em nomes dentro da minha Tabela
    """
    return texto.capitalize().replace(':','').replace('-','').strip()

def padronizar_telefones(numeros):
    """
    Padrinizar os Telefones da minha Tabela, já que ela recebe informações diretas de um Formulário, pode conter erros dos Clientes.

    Args:
    numeros : Telefones > Pensado para ser usado em um For dentro de uma tabela.

    Return : Retorna o Telefone destacando o DDD e removendo quaisquer caracter especial. | Considerando alertar erros de digitação se o Telefone não tiver 11 Numeros(padrão Telefone Brasileiro atual) o programa vai retonar o telefone tratado com um '*' antes do número.
    """
    while '(' in numeros or '-' in numeros or ' ' in numeros or ')' in numeros:
        if '(' in numeros:
            numeros = numeros.replace('(', '')
        if '-' in numeros:
            numeros = numeros.replace('-', '')
        if ' ' in numeros:
            numeros = numeros.replace(' ', '')
        if ')' in numeros:
            numeros = numeros.replace(')', '')
    if len(numeros) == 11:
        numeros = '('+numeros[:2]+')'+numeros[2:]
        return numeros
    elif len(numeros) == 9:
        numeros = numeros[:1]+' '+numeros[1:]
        return numeros
    else:
        return '* ' + numeros
def remover_espacos(dataframe):
    """
    Remover Enter ou espaços vazios dentro das minhas células.

    Arg: 
    dataframe : Tabela que receberá o tratamento.
    """
    dataframe = dataframe.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["",""], regex=True, inplace=True)
    return