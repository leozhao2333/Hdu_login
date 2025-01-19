from Crypto.Cipher import AES
import base64
import json


# 解密密码
def decrypt_password():
    # 从文件中读取密钥
    with open("encryption_key.key", "rb") as key_file:
        key = key_file.read()
    # 读取存储的加密密码数据
    with open("encrypted_password.json", "r") as f:
        encrypted_data = json.load(f)
    # 从文件中读取加密数据
    ciphertext = base64.b64decode(encrypted_data['ciphertext'])
    nonce = base64.b64decode(encrypted_data['nonce'])
    tag = base64.b64decode(encrypted_data['tag'])
    # 使用密钥进行解密
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_password = cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
    return decrypted_password


# 示例：解密密码实验


decrypted_password = decrypt_password()
# print(f"解密后的密码: {decrypted_password}")
