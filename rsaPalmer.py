from os import path
import rsa
import base64
#from dotenv import load_dotenv, find_dotenv

def Get_RSAKey(path_name='/content/drive/MyDrive/BootCampSpot', public_key=True, nbits=4096, create_keys=False):
    pub_file = path_name+'/public.pem'
    prv_file = path_name+'/private.pem'
    (pubkey, privkey) = (None,None)

    exist_pub = path.exists(pub_file)
    exist_prv = path.exists(prv_file)

    if exist_pub:
      #print(f"File Exists {pub_file}")
      pass

    if exist_prv:
      #print(f"File Exists {prv_file}")
      pass

    if (not exist_pub) and (not exist_prv):
      if create_keys:
        (pubkey, privkey) = rsa.newkeys(nbits)
        
        pub = pubkey.save_pkcs1()
        pubfile = open(pub_file,'w+')
        pubfile.write(pub.decode('UTF-8'))
        pubfile.close()
        
        pri = privkey.save_pkcs1()
        prifile = open(prv_file,'w+')
        prifile.write(pri.decode('UTF-8'))
        prifile.close() 

        if public_key:
          return pubkey
        else:
          return privkey
      else:
        print(f"Not creating file(s)")
        return None
    else:
      if public_key and exist_pub:
        # read and return the public key
        with open(pub_file) as fp:
          publicKey = rsa.PublicKey.load_pkcs1(fp.read().encode('UTF-8'))
        return publicKey
      elif (public_key==False) and exist_prv:
        # read and return the private key
        with open(prv_file) as fp:
          privateKey = rsa.PrivateKey.load_pkcs1(fp.read().encode('UTF-8'))
        return privateKey
      else:
        print(f"Didn't find the key to work with")

def Encrypt(data_2_enc:str = None, path_name='/content/drive/MyDrive/BootCampSpot'):
    publicKey = Get_RSAKey(path_name=path_name)

    if (data_2_enc is None) or (publicKey is None):
        return None

    return rsa.encrypt(data_2_enc.encode('UTF-8'), publicKey) #.decode()

def Decrypt(data_2_decrypt= None, path_name='/content/drive/MyDrive/BootCampSpot'):
    privateKey = Get_RSAKey(path_name= path_name, public_key=False)

    if (data_2_decrypt is None) or (privateKey is None):
        return None

    return rsa.decrypt(data_2_decrypt, privateKey).decode()

def Get_API_Key(key_name="QUANDL_API_KEY", env_file='/content/drive/MyDrive/BootCampSpot/.env'):
  if load_dotenv(find_dotenv(filename=env_file)): #, raise_error_if_not_found=True)):
    val = os.getenv(key_name)
    if type(val) == str:
      return True, val
    else:
      print(f'key not found {key_name}')
      return False, (f'key not found {key_name}')
  else:
    return False,  (f'enviroment file missing {env_file}')

# pub_key = Get_RSAKey(path_name=".", public_key=True, nbits=1024, create_keys=False)
# prv_key = Get_RSAKey(path_name=".", public_key=False)

a = "This is a test"

a_enc = Encrypt(a,     path_name=".")
a_dec = Decrypt(a_enc, path_name=".")
print(a, a_enc)
print(a, a_dec)
