import hashlib

def Hkey(data:str):
    result = hashlib.md5(data.encode())
    arrb = result.hexdigest()
    return str(arrb)

debug_key_current = "Luis12345"