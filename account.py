import re
from string import punctuation


class Admin:
    __slots__ = ('__login', '__name', '__surname', '__password')

    def __init__(self, login, name, surname, password):
        self.__login = self.check_log_name_last(login)
        self.name = name
        self.surname = surname
        self.password = password

    @staticmethod
    def check_log_name_last(word: str) -> str:
        """
        :param word: login, name or surname
        :return:
        """
        flag_word = word
        terminal_word = ''.join([x[0].upper() + x[1:] + ':' for x in ['login', 'name', 'surname'] if x == word])
        while True:
            try:
                word = flag_word
                word = input(f">>>{terminal_word}")
                if word == 'q':
                    break
                elif bool(re.findall(f"[^a-zA-Z0-9_]", word)) is True:
                    raise ValueError
                elif len(word) < 3 or not len(word) < 14:
                    raise Exception
                return word
            except ValueError:
                print('>>>Only letters, digits and _ sign are accepted')
            except Exception:
                word = flag_word
                print(f">>>{terminal_word} should be more than 3 characters and less than 8")
            except KeyboardInterrupt:
                print("How is going?")

    @staticmethod
    def checking_pass():
        """
        :return:
        """
        while True:
            try:
                password = input(">>>Password:")
                if password == 'q':
                    break
                elif not bool(re.findall(f"(?=.*[0-9])(?=.*[{punctuation}])", password)):
                    raise ValueError
                elif len(password) < 5 or not len(password) < 16:
                    raise Exception
                return password
            except ValueError:
                print('>>>At least one special character and one digit')
            except Exception:
                print('>>>Password length should be more than 5 and less than 16')
            except KeyboardInterrupt:
                print("Easy go")

    """ login:
        1. getter
    """
    @property
    def login(self):
        return self.__login

    """ name:
        1. getter
        2. setter
        3. deleter
    """
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = self.check_log_name_last(name)

    @name.deleter
    def name(self):
        print(">>>Name can't be deleted")

    """ surname:
        1. getter
        2. setter
    """
    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, surname: str):
        self.__surname = self.check_log_name_last(surname)

    """ password:
        1. getter
        2. setter
    """
    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = self.checking_pass()


class Operator(Admin):
    __slots__ = ('__work_time',)

    def __init__(self, login, name, surname, password, work_time):
        super().__init__(login, name, surname, password)
        self.work_time = work_time

    @staticmethod
    def check_work_time():
        """
        :return:
        """
        time_pattern = '(0[6-9]|1[0-9]|2[0-3]):[0-5][0-9]'
        check_pattern = re.compile('^' + time_pattern + '-' + time_pattern + '$')
        while True:
            try:
                time = input(">>>Worktime:").strip()
                time_check = check_pattern.match(f'{time}')
                if time_check:
                    return time_check.group(0)
                else:
                    raise ValueError
            except ValueError:
                print(">>>Only in from 06:30-23:59, 24 hours format")
            except KeyboardInterrupt:
                print(">>>Lunch time")

    """ Work time:
        1. getter
        2. setter
    """
    @property
    def work_time(self):
        return self.__work_time

    @work_time.setter
    def work_time(self, work_time):
        self.__work_time = self.check_work_time()
