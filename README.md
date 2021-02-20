# file_encryptor

File encryptor is a program that can encrypt and decrypt your files/directories on your computer.
It uses the fernet encryption algorithm to obscure the data in your files/folders as ciphertext (unreadable gibberish).
And you can later use it to decrypt your files whenever you need to use them.

File encryptor is a password based, that means that all processes, whether encryption/decryption are going to require a password to execute.
The same password that was used for encrypting a file is the same password that will be used for decrypting your files and vice versa.

By simply giving the program an:
* action(encryption/decryption)
* filepath(file/folder)
* password

   ... file encryptor will execute your process on all your chosen file/files.

### How to run the program
1. Open up your command prompt and git clone the project onto your local machine.
   ```
   git clone https://github.com/Caleb-Mwasikira/file_encryptor.git
   ```
   This will create a folder called file_encryptor on your machine.
   
2. Navigate into the folder by running:
   ```
   cd ./file_encryptor
   ```
   
3. To run file_encryptor's command line interface type the following command into your terminal:
   ```
   python file_encryptor_cli.py -a [ACTION] -f [FILEPATH]
   ```
   
4. To run the graphical user-interface, change directory into the dist folder and run the file_encryptor .exe / .dmg / .app file
   ```
   cd ./dist 
   ./file_encryptor
   ```
   

**Note: Substitute ACTION with either encrypt or decrypt
      and FILEPATH with C:/User/JohnS/plans/evil.txt**
      
Examples:   
- **Encryption**
    ~~~~
    python file_encryptor_cli.py -a encrypt -f .\data\evil.txt
    python file_encryptor_cli.py -a encrypt -f .\data
    ~~~~
    
    
- **Decryption**
    ~~~~
    python file_encryptor_cli.py -a decrypt -f .\data\(encrypted)evil.txt
    python file_encryptor_cli.py -a decrypt -f .\data
    ~~~~
    
4. Once you run the file_encryptor_cli.py successfully, the program is going to request that you enter a password.
   The password is what is going to be used to encrypt/decrypt your files. Enter your password to contine.
   
   Note: 
     The password can also be set as an environment variable.
     This can be done by typing 
     ```
     set PASSWORD=yoursecretpassword;
     ```
     before running the program.

That's all for now.
Happy hacking!

> **Facta Non Verba!**
    
