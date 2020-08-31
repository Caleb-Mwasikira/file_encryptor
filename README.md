# file_encryptor

File encryptor is a program that can encrypt and decrypt your files/directories on your computer.
It uses the fernet encryption algorithm to obscure the data in your files/folders as ciphertext (unreadable gibberish).
And you can later use it to decrypt your files whenever you need to use them.

File encryptor is a password based, that means that all processes, whether encryption/decryption are going to require a password to execute.
The same password that was used for encrypting a file is the same password that will be used for decrypting your files and vice versa.

By simply giving the program a:
* process(encryption/decryption)
* filepath(file/folder)
* password

   ... file encryptor will execute your process on all your chosen file/files.

### How to run the program
1. Open up your command prompt
2. Navigate to where the file file_encryptor.py is located on your machine.
3. Run the command;

   ```python file_encryptor.py -p [PROCESS] -f [FILEPATH]```

**Note: Substitute PROCESS with either encrypt or decrypt
      and FILEPATH with C:/User/JohnS/plans/evil.txt**
      
Examples:   
- **Encryption**
    ~~~~
    python file_encryptor.py -p encrypt -f .\data\evil.txt
    python file_encryptor.py -p encrypt -f .\data
    ~~~~
    
    
- **Decryption**
    ~~~~
    python file_encryptor.py -p decrypt -f .\data\(encrypted)evil.txt
    python file_encryptor.py -p decrypt -f .\data
    ~~~~
    
4. Once you run the file_encryptor.py successfully, the program is going to request that you enter a password.
   The password is what is going to be used to encrypt/decrypt your files. Enter your password to contine.
   
   Note: 
     The password can also be set as an environment variable.
     This can be done by typing ```set PASSWORD=yoursecretpassword;```
     before running the program.

That's all for now.
Happy hacking!

> **Facta Non Verba!**
>> **Deeds not words!**
    