from cryptography.fernet import Fernet

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path, initial_values=None):
        self.password_file = path

        if initial_values is not None:
            for key, values in initial_values.items():
                self.add_password(key, values)

    def load_password_file(self, path):
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(':')
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(f'{site}:{encrypted.decode()}\n')

    def get_password(self, site):
        return self.password_dict.get(site, None)

def main():
    passwords = {
        'email': '1234567',
        'facebook': 'mypasswordf',
        'youtube': 'helloguys123',
        'otherthing': 'myfavoritepassword12345'
    }

    pm = PasswordManager()

    print("""Ne yapmak istersiniz?
          (1) yeni anahtar oluştur
          (2) var olan anahtarı yükle
          (3) yeni parola dosyası oluştur
          (4) var olan parola dosyasını yükle
          (5) yeni parola ekle
          (6) parola al
          (ç) çıkış
           """)

    done = False

    while not done:
        choice = input('Seçimi tuşlayınız: ')
        if choice == '1':
            path = input('Yolu giriniz: ')
            pm.create_key(path)
        elif choice == '2':
            path = input('Yolu giriniz: ')
            pm.load_key(path)
        elif choice == '3':
            path = input('Yolu giriniz: ')
            pm.create_password_file(path, passwords)
        elif choice == '4':
            path = input('Yolu giriniz: ')
            pm.load_password_file(path)
        elif choice == '5':
            site = input('Siteyi giriniz: ')
            password = input('Parolayı giriniz: ')
            pm.add_password(site, password)
        elif choice == '6':
            site = input('Hangi siteyi istersiniz: ')
            password = pm.get_password(site)
            if password:
                print(f'{site} için parola: {password}')
            else:
                print(f'{site} için parola bulunamadı.')
        elif choice == 'ç':
            done = True
            print('Çıkılıyor...')
        else:
            print('Geçersiz seçenek')

if __name__ == '__main__':
    main()
