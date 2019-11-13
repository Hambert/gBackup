from cryptography.fernet import Fernet

def encrypt_file(input_file = 'test.txt', key = b''):
	#key = b'' # Use one of the methods to get a key (it must be the same when decrypting)
	#input_file = 'test.txt'
	print(input_file)
	
	output_file = input_file + '.enc'

	with open(input_file, 'rb') as f:
	    data = f.read()

	fernet = Fernet(key)
	encrypted = fernet.encrypt(data)

	with open(output_file, 'wb') as f:
	    f.write(encrypted)

def decrypt_file(input_file, output_file, key):

	with open(input_file, 'rb') as f:
	    data = f.read()

	fernet = Fernet(key)
	encrypted = fernet.decrypt(data)

	with open(output_file, 'wb') as f:
	    f.write(encrypted)

if __name__ == '__main__':

	#key = '0123456789abcdef'
	key = Fernet.generate_key()
	print(key)

	encrypt_file("credentials.json", key)

	decrypt_file("credentials.json.enc", "neu_credentials.json", key)
