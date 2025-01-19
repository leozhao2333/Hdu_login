from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import getpass
import base64
import json


# 加密密码并存储
def encrypt_password(password, key):
    # 生成一个随机的盐（加密时使用）
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(password.encode())
    # 将加密后的密码、盐、tag一并存储
    encrypted_data = {
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
        'nonce': base64.b64encode(cipher.nonce).decode('utf-8'),
        'tag': base64.b64encode(tag).decode('utf-8')
    }

    # 存储加密数据到文件
    with open("encrypted_password.json", "w") as f:
        json.dump(encrypted_data, f)
    print("密码已加密并存储！")


# 示例
password = getpass.getpass(prompt="请输入密码：")
key = get_random_bytes(16)  # 生成一个 16 字节的密钥，用于 AES 加密

# 保存密钥到文件
with open("encryption_key.key", "wb") as key_file:
    key_file.write(key)

encrypt_password(password, key)
