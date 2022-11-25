import json

# CRUD in dict table (create, read, update, delete, save, load)
# table => {<id_1>: {<field_1>: <value_1>, <field_2>: <value_2>, ...}, ...}
# fields => {<field_1>: <type_1>, <field_2>: <type_2>, ...}
# field name `id´ is reserved


def crud_create(table, fields, register=None,
                fields_error="Not all fields in register."):
    ''' id is autonum '''
    id_pk = (len(table) and max(table)) + 1
    if not register:
        register = {}   
        for field, cast in fields.items():
            while True:
                try:
                    register[field] = cast(input(f"{field.capitalize()}: "))
                    break
                except Exception:
                    print(f"😔 [{cast.__name__}]")
    if not all(f in register for f in fields):
        print(f"***** {fields_error} *****")
        return False
    table[id_pk] = register
    return True


def crud_read(table, search=None, empty="List is empty", just_verify=False):
    ''' search => {field: search} '''
    if search:
        field, value = list(search.items())[0]
        if field == 'id':
            if isinstance(value, str) and value.isdigit():
                value = int(value)
            result_set = ((value, table[value]),) if value in table else None
        else:
            result_set = tuple(filter(
                lambda r: str(value).lower() in str(r[1][field]).lower(),
                table.items()))
    else:
        result_set = table.items()
    if just_verify:
        return bool(result_set)
    if not result_set:
        print(f"{'-':->50}")
        print(f"***** {empty} *****")
        print(f"{'=':=>50}")
        return False
    for id_pk, register in result_set:
        print(f"{'-':->50}")
        print(f"Id: {id_pk}")
        for field, value in register.items():
            print(f"{field.capitalize()}: {value}")
    print(f"{'=':=>50}")
    return True


def crud_update(table, id_pk, register=None, fields=None,
                not_found="not found.",
                fields_error="Not all fields in register."):
    if id_pk not in table:
        print(f"***** {id_pk} {not_found} *****")
        return False
    if not register:
        register = table[id_pk]
        for field, value in register.items():
            cast = type(value)
            while True:
                try:
                    new = input(f"{field.capitalize()} [{value}]: ")
                    if new:
                        register[field] = cast(new)
                    break
                except Exception:
                    print(f"😔 [{cast.__name__}]")
        return True
    if not all(f in register for f in fields):
        print(f"***** {fields_error} *****")
        return False
    table[id_pk] = register
    return True


def crud_delete(table, id_pk, not_found="not found"):
    if id_pk not in table:
        print(f"***** {id_pk} {not_found} *****")
        return False
    del table[id_pk]
    return True


def crud_save(table, file_name="dict_crud.json"):
    try:
        with open(file_name, 'w') as f:
            json.dump(table, f, indent=4)
    except Exception:
        return False
    return True


def crud_load(table, file_name="dict_crud.json"):
    if True:  # try:
        table.clear()
        with open(file_name, 'r') as f:
            table.update({int(k): v for k, v in json.load(f).items()})
    else:  # except Exception:
        return False
    return True


# Teste

if __name__ == '__main__':

    # Variáveis globais para teste
    tabela = {}
    campos = {'nome': str, 'idade': int, 'filhos': int, 'salário': float}
    opcoes = ('Menu', 'Listar', 'Filtrar', 'Inserir', 'Atualizar', 'Deletar',
              'Carregar', 'Salvar', 'Sair')

    # Funções para teste do CRUD com menu

    def listar():
        crud_read(tabela, empty="Listagem vazia!")

    def filtrar():
        print("0. Id")
        for n, campo in enumerate(campos):
            print(f"{n + 1}. {campo.capitalize()}")
        try:
            n = int(input("Por qual campo filtrar? "))
            campo = (['id'] + list(campos))[n]
            valor = input(f"O que procurar em `{campo.capitalize()}´? ")
            crud_read(tabela, {campo: valor}, empty="Listagem vazia!")
        except Exception:
            print("*** Erro! ***")

    def inserir():
        crud_create(tabela, campos)

    def atualizar():
        listar()
        try:
            id_pk = int(input("Qual deseja alterar? "))
            if crud_update(tabela, id_pk, not_found="não encontrado!"):
                print("****** Alterado com sucesso! *****")
        except Exception:
            print("*** Erro! ***")

    def deletar():
        listar()
        try:
            id_pk = int(input("Qual deseja deletar? "))
            if crud_delete(tabela, id_pk, not_found="não encontrado!"):
                print("****** Excluído com sucesso! *****")
        except Exception:
            print("*** Erro! ***")

    def carregar():
        crud_load(tabela)
        listar()

    def salvar():
        listar()
        if crud_save(tabela):
            print("***** Salvo com sucesso! *****")
        else:
            print("***** Erro ao salvar! *****")

    def main():
        menu()
        while True:
            opcao = menu(False, True)
            if opcao == len(opcoes) - 1:
                break
            globals()[opcoes[opcao].lower()]()

    def menu(mostar=True, perguntar=False):
        largura = max(map(len, opcoes))
        if mostar:
            print(f"|{'-':->{largura + 3}s}|")
            print('\n'.join(f"|{n}. {opcao:{largura}s}|"
                            for n, opcao in enumerate(opcoes)))
        while perguntar:
            print(f"|{'-':->{largura + 3}s}|")
            try:
                opcao = int(input("| Opção: "))
                assert 0 <= opcao < len(opcoes)
                return opcao
            except Exception:
                print(f"|{' Inválida':{largura + 3}s}|")
                menu()

    main()
