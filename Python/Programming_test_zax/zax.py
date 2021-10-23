import datetime



def le_dados_loja(lojas):                                                                                                                               # a query para fazer a busca dos dados da loja deve receber as lojas como parametro para buscar os dados da lojas que possuem pedido
    dados_loja = (('loja_1', 0.05), ('loja_2', 0.05), ('loja_3', 0.15))                                                                                 # esses dados devem ficar em algum banco de dados a query deveria ler as columnas do nome/id da loja e a percentagem da comissao
    return {loja: comissao for loja, comissao in dados_loja}


def le_dados_motoboy():
    dados_motoboy = (('moto_1', 2, None), ('moto_2', 2, None), ('moto_3', 2, None), ('moto_4', 2, 'loja_1'), ('moto_5', 2, None))                       # esses dados devem ficar em algum banco de dados a query deveria ler as columnas do nome/id da motoboy, custo da entrega e o nome/id da loja se o motorista tem exclusividade, None se não possui
    return {moto: (fixo_entrega, loja_exclusividade) for moto, fixo_entrega, loja_exclusividade in dados_motoboy}


def le_pedidos(data=datetime.date.today()):                                                                                                             # a query para fazer a busca dos pedidos deve receber a data como parametro para buscar os pedidos para o dia
    pedidos = ((1, 'loja_1', 50), (2, 'loja_1', 50), (3, 'loja_1', 50),                                                                                 # esses dados devem ficar em algum banco de dados a query deveria ler as columnas do id do pedido, nome/id da loja, valor da entrega para o dia
               (1, 'loja_2', 50), (2, 'loja_2', 50), (3, 'loja_2', 50), (4, 'loja_2', 50),
               (1, 'loja_3', 50), (2, 'loja_3', 50), (3, 'loja_3', 100))
    return pedidos


def calcula_valor_entrega(valor_entrega, comissao_loja, fixo_motoboy):
    return valor_entrega * comissao_loja + fixo_motoboy


def seleciona_motoboy(motoboy_pedidos, motoboys):
    selecionado = list()

    for moto in motoboys:
        if not motoboy_pedidos.get(moto):
            return moto

        if not selecionado or motoboy_pedidos.get(moto, 0) < selecionado[1]:
            selecionado = [moto, motoboy_pedidos[moto]]

    if not selecionado:
        selecionado = [motoboys[0]]

    return selecionado[0]


def atribui_pedido_a_moto(moto, pedido, entregas, motoboy_pedidos, comissao_loja, fixo_motoboy):
    motoboy_pedidos.setdefault(moto, 0)
    entregas.setdefault(moto, {})

    motoboy_pedidos[moto] += 1
    entregas[moto].setdefault(pedido[1], []).append([pedido[0], calcula_valor_entrega(pedido[2], comissao_loja, fixo_motoboy)])

def verifica_exclusividade(loja_exclusividade, loja, motoboy_pedidos, min_pedido_por_moto):
    if (moto := loja_exclusividade.get(loja, False)) and motoboy_pedidos.get(moto, 0) < min_pedido_por_moto:
        return moto


def distribui_pedidos(pedidos, dados_loja, dados_motoboy):
    loja_exclusividade = {dados[1]: moto for moto, dados in dados_motoboy.items() if dados[1] is not None}
    motoboys = list(dados_motoboy.keys())

    entregas = dict()
    motoboy_pedidos = dict()
    min_pedido_por_moto = len(pedidos) // len(motoboys) + (1 if len(pedidos) % len(motoboys) else 0)                                                    # adiciona 1 se o resto não for zero pois o motoboy com exclusividade deve ter preferência

    for pedido in pedidos:
        comissao_loja = dados_loja[pedido[1]]

        if (moto := verifica_exclusividade(loja_exclusividade, pedido[1], motoboy_pedidos, min_pedido_por_moto)):
            atribui_pedido_a_moto(moto, pedido, entregas, motoboy_pedidos, comissao_loja, dados_motoboy[moto][0])

        else:
            moto = seleciona_motoboy(motoboy_pedidos, motoboys)
            atribui_pedido_a_moto(moto, pedido, entregas, motoboy_pedidos, comissao_loja, dados_motoboy[moto][0])

    return entregas


def imprime_dados_entrega(moto, dados_entregas):
    print(f'Motoboy: {moto}')
    total_pedidos = 0
    total_valor = 0
    for loja, pedidos in dados_entregas.items():
        print(f'\tLoja: {loja}')
        for pedido, valor in pedidos:
            print(f'\t\tPedido: {pedido}')
            print(f'\t\tValor: {valor}')
            print('\t\t----------------------')

            total_pedidos += 1
            total_valor += valor

    print(f'\tTotal de pedidos: {total_pedidos}')
    print(f'\tValor total: {total_valor}')
    print('\n')


def main():
    pedidos = le_pedidos()
    dados_loja = le_dados_loja([pedido[1] for pedido in pedidos])
    dados_motoboy = le_dados_motoboy()


    entregas = distribui_pedidos(pedidos, dados_loja, dados_motoboy)

    while True:
        print('Insira o nome/id do motoboy para verificar as entregas, '
              'vazio para verificar as entregas de todos os motoboys '
              'ou Sair para encerrar o programa')
        comando = str(input())
        print('\n')

        if comando == '':
            for motoboy in entregas:
                imprime_dados_entrega(motoboy, entregas[motoboy])

        elif entregas.get(comando):
            imprime_dados_entrega(comando, entregas[comando])

        elif comando.upper() == 'SAIR':
            break

        else:
            print(f'Motoboy {comando} não encontrado, verifique se o nome está correto.')
            print('\n')

main()