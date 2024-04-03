import re
from account import Admin, Operator


class Market:
    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

        self.cu_basket = []
        self.total_price = 0

        self.gr_limit = [0.00, 100.00]
        self.un_limit = list(range(1, 101))

        self.pr_per_gr = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6']
        self.pr_per_unit = ['p7', 'p8']

        self.accounts = {}
        self.acc_count = 0

        self.invoices = {}
        self.shifts = {}

        self.id_products = {
            'p1': 'tomato',
            'p2': 'potato',
            'p3': 'cucumber',
            'p4': 'orange',
            'p5': 'choco',
            'p6': 'candies',
            'p7': 'bread',
            'p8': 'butter',
        }

        self.products_prices = {
            'tomato': 1.20,
            'potato': 2.75,
            'cucumber': 10.50,
            'orange': 3.20,
            'choco': 2.00,
            'candies': 4.50,
            'bread': 1.20,
            'butter': 3.90,
        }

        self.promo_price = {
            'tomato': 0.5,
            'candies': 0.33,
            'butter': 0.23,
            'cucumber': 0.1,
        }

    @staticmethod
    def press_enter():
        while True:
            try:
                terminal_input = input('\n>>>Press enter to continue\n')
                if len(terminal_input) == 0:
                    break
                elif terminal_input != '':
                    print(">>>Only enter to press")
            except KeyboardInterrupt:
                print("0_O")

    def show_stocks(self) -> str:
        return ''.join([f'{x}:' + ' {}\n' for x in self.id_products.keys()]).format(*self.id_products.values())

    def show_basket(self) -> str:
        output = ''
        for en, (product, gr_un) in enumerate(self.cu_basket, 1):
            f_price = round(gr_un * self.products_prices[self.id_products[product]], 2)
            per_promo = f'-{int(self.promo_price[self.id_products[product]] * 100)}%' if self.id_products[
                                                                                             product] in self.promo_price else ''
            promo_price = f_price - round(f_price * self.promo_price[self.id_products[product]], 1) if len(
                per_promo) > 0 else ''
            list_for_spaces = [self.id_products[product] + str(self.products_prices[self.id_products[product]]),
                               str(gr_un), str(promo_price) + str(per_promo) if len(str(per_promo)) else str(f_price)]
            spaces_all = [' ' * (n - len(l)) for n, l in zip([17, 8, 12], list_for_spaces[::])]
            ans = f'{en}.  {self.id_products[product]}{spaces_all[0]}{self.products_prices[self.id_products[product]]}€\
   x{spaces_all[1]} {gr_un}     {per_promo}   {spaces_all[2]}{promo_price if len(str(promo_price)) > 0 else f_price}€'
            self.total_price += promo_price if len(str(promo_price)) > 0 else f_price
            output += ans + '\n'
        return output

    def del_el_basket(self):
        while True:
            print(self.show_basket())
            print('>>>Which element by number of line would you like to delete?')
            try:
                num = input('Enter:')
                if num == 'q':
                    break
                self.cu_basket.pop(int(num) - 1)
                return self.cu_basket
            except IndexError:
                print('>>>No such element in basket')
                print('___________________________________________________')
            except ValueError:
                print('>>>Only integer')
            except KeyboardInterrupt:
                print('>>>Tea time')

    def show_total_price(self) -> str:
        self.total_price = 0
        basket = re.sub('\d{1,3}[.]\s\s', '', self.show_basket())
        line = 52 * '-'
        spaces_all = [21 * ' ', 18 * ' ', 20 * ' ',
                      (29 - (len(str(round(self.total_price, 1)))) + len('Total price')) * ' ']
        return (
            f"{spaces_all[0]}{self.name}\n{spaces_all[1]}{self.address}\n{spaces_all[2]}{self.phone}\n{line}\n{basket}\n"+\
            f"{line}\nTotal price{spaces_all[3]}{round(self.total_price, 2)}€")

    """Main
    """
    def manage_basket(self, acc):
        print('__________________________________________')
        print(self.show_stocks())
        print(">>>Please enter products id and quantity/grammar\n"+\
              "__________________________________________")
        print('>>>c - calculate, d - delete stock')
        self.cu_basket = []
        self.total_price = 0
        while True:
            try:
                terminal_input = input('\nPush enter to start\n>>>')
                if len(terminal_input) == 0:
                    break
                elif terminal_input == 'q':
                    break
                elif terminal_input != '':
                    print(">>>Press enter or q to quite")
            except KeyboardInterrupt:
                print('Where are you going ? ^^')

        if terminal_input == 'q':
            return print('Have a nice day : )\n')

        while True:
            stock = self.check_stock()
            if stock == 'c':
                break
            elif stock == 'q':
                return
            elif stock is not None and len(stock) == 2 and type(stock) == list:
                self.cu_basket.append(stock)
                print('')
                print(self.show_basket())

        if stock == 'q':
            return

        while True:
            try:
                terminal_input = input('>>>Calculate?')
                if len(terminal_input) == 0:
                    pass
                elif terminal_input == 'q':
                    self.cu_basket = []
                    self.total_price = 0
                    break
                elif terminal_input != '':
                    print(">>>Press enter or q to quite")
            except KeyboardInterrupt:
                print("What's up ? =)")
            else:
                print(self.show_total_price())
                self.cu_basket = []
                self.total_price = 0
                self.press_enter()
                break

    def check_stock(self):
        pr_id = self.check_id_stock()
        if pr_id in self.pr_per_gr:
            gr = self.check_gr()
            if gr is not None:
                return [pr_id, gr]
        elif pr_id in self.pr_per_unit:
            un = self.check_unit()
            if un is not None:
                return [pr_id, un]
        return pr_id

    def check_id_stock(self):
        while True:
            try:
                pr_id = input('>>>Product id:').strip()
                if pr_id == 'c':
                    return pr_id
                elif pr_id == 'q':
                    return pr_id
                elif pr_id == 'd':
                    self.del_el_basket()
                elif pr_id not in self.id_products:
                    print('>>>Error: There is no such id in list with actual products or type q to quit')
                return pr_id
            except KeyboardInterrupt:
                print("hm..not this time")

    def check_gr(self):
        while True:
            try:
                gr = input('>>>kg/gr:').strip()
                if gr == 'q':
                    break
                gr = (lambda x: x if self.gr_limit[0] < float(x) <= self.gr_limit[1] else False)(gr)
                if gr is False:
                    print('>>>Error: Only float type [0.01-100.00] or q to quit')
                return float(gr)
            except KeyboardInterrupt:
                print("(=")

    def check_unit(self):
        while True:
            try:
                un = input('>>>Quantity:').strip()
                if un == 'q':
                    break
                un = self.un_limit.index(int(un))
                return un + 1
            except ValueError:
                print('>>>Error: Only Integer type [1-100] or  write in q to quit')
            except KeyboardInterrupt:
                print("(づ｡◕‿‿◕｡)づ")

    def show_id(self):
        print('\n' + '\n'.join([f'{x}:' + ' {}' for x in self.id_products.keys()]).format(*self.id_products.values()))
        self.press_enter()

    def show_prices(self):
        print('\n' + '\n'.join([f'{x}:' + ' {}€' for x in self.products_prices.keys()]).format(
            *self.products_prices.values()))
        self.press_enter()

    def add_stock(self):
        while True:
            try:
                product = input('>>>Enter product name:')
                if product == 'q':
                    break
                check_exist = True if product in self.id_products.values() else False
                if check_exist is False:
                    print('>>>Price')
                    price = float(input('>>>'))
                    number = f'p{[k[1] for k in self.id_products.keys()][-1]}'
                    self.id_products[number] = product
                    self.products_prices[product] = price
                else:
                    print('>>>This product already exists')
            except ValueError:
                print('>>>Only float type')
            except KeyboardInterrupt:
                print('>>>bool(Today)')

    def del_stock(self):
        while True:
            try:
                product = input('>>>Product number:')
                if product == 'q':
                    break
                check_exist = True if product in self.id_products.keys() else False
                if check_exist:
                    del self.products_prices[self.id_products[product]]
                    del self.promo_price[self.id_products[product]]
                    del self.id_products[product]
                    print(self.show_basket())
                else:
                    print('>>>There is no such product')
            except KeyboardInterrupt:
                print('>>>This is just KeyboardInterrupt')

    def show_promo(self):
        print('\n' + '\n'.join([f'{x}:' + ' {}%' for x in self.promo_price.keys()]).format(*self.promo_price.values()))
        self.press_enter()

    def add_promo(self):
        while True:
            try:
                product = input('>>>Enter product name:')
                if product == 'q':
                    break
                check_exist = True if product in self.promo_price.keys() else False
                if check_exist is False:
                    promo = float(input('>>>Promo:'))
                    self.promo_price[product] = promo
                else:
                    print('>>>This product is already exists')
            except ValueError:
                print('>>>Only float type')
            except KeyboardInterrupt:
                print('>>>:...>_>.......<_<')

    def del_promo(self):
        while True:
            try:
                product = input('>>>Product name:')
                if product == 'q':
                    break
                check_exist = True if product in self.promo_price.keys() else False
                if check_exist:
                    del self.promo_price[product]
                else:
                    print('>>>There is no such product')
            except KeyboardInterrupt:
                print('( ੭ ˙ᗜ˙ )੭ ')

    def show_accounts(self):
        print('\n'.join([f'N{list(self.accounts.items())[i][0]} - Login name:{list(self.accounts.values())[i][0].login}'
                         for i in range(len(self.accounts))]))
        self.press_enter()

    def create_account(self, word):
        while True:
            try:
                e_q = input(">>>Press enter to continue or q to quite:")
                if len(e_q) == 0:
                    if word == 'admin':
                        oAccount = Admin('login', 'name', 'surname', 'password')
                        if oAccount.login not in [list(self.accounts.values())[i][0].login for i in
                                                 range(len(self.accounts))]:
                            self.accounts[self.acc_count] = oAccount, True
                            self.acc_count += 1
                            self.press_enter()
                            break
                        else:
                            print('>>>Login is already exists')
                    elif word == 'operator':
                        oAccount = Operator('login', 'name', 'surname', 'password', 'worktime')
                        if oAccount.login not in [list(self.accounts.values())[i][0].login for i in
                                                 range(len(self.accounts))]:
                            self.accounts[self.acc_count] = oAccount, False
                            self.acc_count += 1
                            self.press_enter()
                            break
                        else:
                            print('>>>Such login is already exists')
                elif e_q == 'q':
                    break
                elif e_q != '':
                    print(">>>Enter or q to quite")
            except KeyboardInterrupt:
                print('How is weather?')

    def delete_acc(self):
        self.show_accounts()
        while True:
            try:
                number = input('>>>Choose account number to delete:')
                if number == 'q':
                    break
                elif number:
                    del self.accounts[int(number)]
            except ValueError:
                print('>>>Only integer type in key range')
            except KeyboardInterrupt:
                print('>>>(ᐢ • ˕ • ᐢ)')
