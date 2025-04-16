from nacl.signing import SigningKey
from base58 import b58encode
from eth_account import Account
from tonsdk.contract.wallet import WalletVersionEnum, Wallets
from tonsdk.utils import bytes_to_b64str
from tonsdk.crypto import mnemonic_new
import os
import time
from pystyle import Colorate, Colors
import ctypes
import random
from solders.keypair import Keypair
import base58

def get_screen_resolution():
    user32 = ctypes.windll.user32
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    return width, height

def move_window_to_center(hwnd, width, height):
    user32 = ctypes.windll.user32
    screen_width, screen_height = get_screen_resolution()
    x = (screen_width - width) // 5
    y = (screen_height - height) // 4
    user32.MoveWindow(hwnd, x, y, width, height, True)

renk_gradyanlari = [
    Colors.yellow_to_red,
    Colors.yellow_to_green,
    Colors.green_to_white,
    Colors.green_to_yellow,
    Colors.green_to_red,
    Colors.blue_to_cyan,
    Colors.cyan_to_blue,
    Colors.blue_to_purple,
    Colors.purple_to_blue,
    Colors.purple_to_red,
    Colors.red_to_purple
]

os.system('mode con: cols=55 lines=50')

window_title = "Crypto Wallet Creator - Play2EarnTR"

ctypes.windll.kernel32.SetConsoleTitleW(window_title)

time.sleep(0.5)

hwnd = ctypes.windll.user32.FindWindowW(None, window_title)

if hwnd:
    screen_width, screen_height = get_screen_resolution()
    move_window_to_center(hwnd, min(420, screen_width), min(550, screen_height))
else:
    print("Belirtilen pencere bulunamadı.")

def banner():
    bannerz = f'''
    {" ▄ .▄ ▄▄▄·   ▄▄ ▪  ·▄▄▄▄ ▪▄▄▄▄. ▀▌ ▐·▪".center(40)}
    {"██▪▐█▐█ ▀█ •█▌▐█   ██▪ ██ █▄.▀·▪█·█▌".center(40)}
    {"██▀▀█▄█▀▀█ ▐█▐▌   ▐█· ▐█▌▐▀▀ ▪▐█▐█•".center(40)}
    {"██ ▐█▐█ ▪▐▌██▐█▌   ██. ██ ▐█▄▄▌ ███ ".center(40)}
    {"▀█▪ █ ▀  ▀ ▀▀ █▪ ▀ ▀▀▀▀▀•  ▀▀▀ . ▀  ".center(40)}
    {"                  x.com/@play2earnTR".center(40)}
    '''
    os.system("cls")
    print(Colorate.Horizontal(Colors.yellow_to_red, bannerz, 1))
    print(Colorate.Horizontal(Colors.yellow_to_red, "═" * 48, 1))
    print("\n")

banner()

def create_metamask_wallets(num_wallets):
    wallets = []
    for i in range(num_wallets):
        account = Account.create()
        public_key = account.address
        private_key = account.key.hex()

        wallets.append({
            'public_key': public_key,
            'private_key': private_key
        })
    return wallets

def create_ronin_wallets(num_wallets):
    wallets = []
    for i in range(num_wallets):
        account = Account.create()
        address = account.address
        private_key = account.key.hex()

        wallets.append({
            'public_key': address,
            'private_key': private_key
        })
    return wallets

def create_ton_wallets(num_wallets):
    wallets = []
    wallet_workchain = 0
    wallet_version = WalletVersionEnum.v3r2

    for i in range(num_wallets):
        wallet_mnemonics = mnemonic_new()
        _, _, _, wallet = Wallets.from_mnemonics(wallet_mnemonics, wallet_version, wallet_workchain)
        address = wallet.address.to_string(True, True, False)

        wallets.append({
            'public_key': address,
            'mnemonics': ' '.join(wallet_mnemonics)
        })
    return wallets

def create_sol_wallets(num_wallets):
    wallets = []
    for i in range(num_wallets):
        new_account = Keypair()
        wallet_address = str(new_account.pubkey())
        private_key_bytes = new_account.secret()
        public_key_bytes = bytes(new_account.pubkey())
        encoded_keypair = private_key_bytes + public_key_bytes
        private_key = base58.b58encode(encoded_keypair).decode()

        wallets.append({
            'public_key': wallet_address,
            'private_key': private_key
        })
    return wallets

def save_wallets_to_file(wallets, wallet_type):
    filename = f"{wallet_type}_wallets.txt"
    with open(filename, "w", encoding="utf-8") as file:
        if wallet_type == "ton":
            file.write(f"address,mnemonics\n")
        else:
            file.write(f"address,private_key\n")
        for i, wallet in enumerate(wallets):
            if wallet_type == "ton":
                file.write(f"{wallet['public_key']},{wallet['mnemonics']}\n")
            else:
                file.write(f"{wallet['public_key']},{wallet['private_key']}\n")

    print(Colorate.Horizontal(Colors.green_to_yellow, f"  Cüzdan bilgileri dosyaya kaydedildi {filename}", 1))

def main():
    print(Colorate.Horizontal(Colors.yellow_to_green, f"  Oluşturmak istediğiniz cüzdan türünü seçin:\n", 1))
    print("\n")
    print(Colorate.Horizontal(Colors.purple_to_blue, f"   1. Solana", 1))
    print(Colorate.Horizontal(Colors.yellow_to_red, f"   2. MetaMask", 1))
    print(Colorate.Horizontal(Colors.blue_to_white, f"   3. Ronin", 1))
    print(Colorate.Horizontal(Colors.cyan_to_blue, f"   4. TON", 1))
    print("\n")

    choice = input(" Seçiminizi girin (1, 2, 3, 4):")
    print("\n")
    num_wallets = int(input("Oluşturmak istediğiniz cüzdan sayısını girin: \n"))

    if choice == '1':
        wallets = create_sol_wallets(num_wallets)
        save_wallets_to_file(wallets, "sol")
    elif choice == '2':
        wallets = create_metamask_wallets(num_wallets)
        save_wallets_to_file(wallets, "metamask")
    elif choice == '3':
        wallets = create_ronin_wallets(num_wallets)
        save_wallets_to_file(wallets, "ronin")
    elif choice == '4':
        wallets = create_ton_wallets(num_wallets)
        save_wallets_to_file(wallets, "ton")
    else:
        print("Geçersiz seçim")

if __name__ == "__main__":
    main()
