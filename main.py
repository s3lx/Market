from sys import exit
from market import Market

oMarket = Market('Best Market', 'Central street 33', '(22) 333-4444')
print(">>>Hi! In order to proceed please create an admin account")

while True:
    try:
        oMarket.create_account('admin')
        if len(oMarket.accounts) == 0:
            exit()
        break
    except KeyboardInterrupt:
        print("=)")

while True:
    check_admin = ''
    login = ''
    name = ''
    surname = ''
    try:
        login = input('>>>Login:').strip()
        password = input('>>>Password:').strip()
        check_login = [[i, el] for i, el in
                       [(i, list(oMarket.accounts.values())[i][0].login) for i in range(len(oMarket.accounts))] if
                       el == login]
        check_login_filter = [el for nested_list in check_login for el in nested_list]
        password = True if password in [list(oMarket.accounts.values())[check_login_filter[0]][0].password for i in
                                        range(len(oMarket.accounts))] else False
        if check_login is False or password is False:
            raise Exception
    except Exception:
        print('>>>Login or password is not correct')
    else:
        check_admin = True if True is list(oMarket.accounts.values())[check_login_filter[0]][1] else False
        login = list(oMarket.accounts.values())[check_login_filter[0]][0].login
        name = list(oMarket.accounts.values())[check_login_filter[0]][0].name
        surname = list(oMarket.accounts.values())[check_login_filter[0]][0].surname

    if check_admin:
        while True:
            print('\n>>>Hi')
            try:
                print(f'>>>Admin: {name} {surname}')
                print("Type:\n\
manage       = manage basket\n\
operator     = create operator account\n\
accounts     = show all accounts\n\
delete acc   = delete account\n\
show id      = products id's\n\
show prices  = products prices\n\
show promo   = products promo\n\
add promo    = add promo for the product\n\
delete promo = delete promo of the product\n\
add stock    = add stock with price\n\
delete stock = delete stock from market\n\
q            = exit")
                terminal_input = input('>>>').strip()
                if terminal_input == 'manage':
                    oMarket.manage_basket(login)
                elif terminal_input == 'operator':
                    oMarket.create_account('operator')
                elif terminal_input == 'admin':
                    oMarket.create_account('admin')
                elif terminal_input == 'accounts':
                    oMarket.show_accounts()
                elif terminal_input == 'delete acc':
                    oMarket.delete_acc()
                elif terminal_input == 'show id':
                    oMarket.show_id()
                elif terminal_input == 'show prices':
                    oMarket.show_prices()
                elif terminal_input == 'show promo':
                    oMarket.show_promo()
                elif terminal_input == 'add promo':
                    oMarket.add_promo()
                elif terminal_input == 'delete promo':
                    oMarket.del_promo()
                elif terminal_input == 'add stock':
                    oMarket.add_stock()
                elif terminal_input == 'delete stock':
                    oMarket.del_stock()
                elif terminal_input == 'q':
                    break

            except Exception:
                print('>>>Admin Error')

    elif check_admin is False:
        while True:
            print('\n>>>Hi')
            try:
                print(f'>>>Operator: {name} {surname}')
                print('Type:\n\
manage = manage basket\n\
q      = exit')
                terminal_input = input().strip()
                if terminal_input == 'manage':
                    oMarket.manage_basket(login)
                elif terminal_input == 'q':
                    break

            except Exception:
                print('>>>Operator error')
