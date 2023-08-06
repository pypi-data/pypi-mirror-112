class Logger:

    def log(self, message):
        print(f'Log - {message}')

    def error(self, message):
        print(f'Error - {message}')

    def debug(self, message):
        print(f'debug - {message}')