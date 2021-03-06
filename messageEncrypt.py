import random
import math
from Crypto.Hash import SHA256

def stringToBitList(message):
    """Converts a string with alphabetic, numeric and special characters to a list of 0's and 1's"""
    total = []
    for character in message:
        # Store Unicode code point of the character in c
        c = ord(character) 
        indiv = []
        # Convert the value in c to binary, and store this binary as a list of 0's and 1's
        while c > 0:
            indiv = [(c % 2)] + indiv
            c = c / 2
        # Pad the binary representation to 8 bits
        indiv = padBits(indiv,8)
        # Sum the padded binary representations of each character 
        total = total + indiv
    return total

def bitListToBinString(bitList):
    """Converts a list of 0's and 1's to a string of '0's and '1's"""
    return ''.join([('0','1')[b] for b in bitList])

def binStringToInt(binString):
    """Converts a string of binary digits to an integer of base 10"""
    return int(binString,2)

def stringToInt(message):
    """Wrapper function for above two funtions to convert a 
    string to a base 10 integer based on the ASCII values of
     its characters"""
    return binStringToInt(bitListToBinString(stringToBitList(message)))

def binstringToBitList(binstring): 
    """Converts a string of '0's and '1's to a list of 0's and 1's"""
    bitList = []
    for bit in binstring:
        bitList.append(int(bit))
    return bitList

def padBits(bits, padding):
    """Pad the input bits with 0's so that it is of length padding"""
    return [0] * (padding-len(bits)) + bits

def bitListToString(paddedBitSeq):
    """Converts a list of 0's and 1's to a string of alpha/numeric characters"""
    charBuilder = ''
    # Iterate through by 8's becaause each padded bit sequence is 8 bits long
    for segment in range(0,len(paddedBitSeq),8): 
        # concatenate each new char onto the built up string
        charBuilder = charBuilder + bitsToChar(paddedBitSeq[segment: segment+8]) 
    return charBuilder

def bitsToChar(bitSeq):
    """Converts each 8 bit length padded bit sequences 
    back to a char based on its unicode value"""
    value = 0
    for bit in bitSeq:
        value = (value * 2) + bit # This for loop will determine the numeric value of the binary bit sequence input
    return chr(value)

def intToString(integer):
    """Wrapper function for above four funtions to convert an i
    nteger of base 10 to a string based on the ASCII values of 
    its characters"""
    binary = bin(integer)[2:]
    bitSeq = binstringToBitList(binary)
    return bitListToString(padBits(bitSeq,(len(bitSeq)+(8-(len(bitSeq)%8)))))

def extendedGCD(a, b):
    """Returns gcd, x and y so that a*x+b*y = gcd(x,y)"""
    # Base case (when a = 0)
    if a == 0:
        return (b,0,1)
    # Recursive case
    else:
        gcd, x, y = extendedGCD(b%a,a)
        return (gcd, y-(b/a)*x, x)

def modularInverse(a,mod):
    """Returns the value whose product with (a % mod) is equal to 1"""
    gcd,x,y = extendedGCD(a,mod)
    return x%mod

def isPrime(num):
    """"Return True if the number is prime, and False otherwise."""
    # Two basic cases where number can be quickly seen as prime or not prime
    if (num<2):
        return False
    elif num%2==0:
        return num == 2 # Two is the only even prime number

    # Start of Rabin Miller Primality Test
    s = num - 1
    counter1 = 0
    # if s is even keep halving it
    while s%2 == 0:
        s = s/2
        # increment counter1
        counter1 += 1 
    trial = 8 # Number of times we will check num's primailty. Accuracy is improved with increased trials
    while trial>0:
        rando = random.randrange(2,num)
        modNum = pow(rando,s,num) # modNum is equal to rando^r mod num
        if modNum != 1: # Rabin miller test does not apply if v = 1
            counter2 = 0
            while modNum != (num - 1):
                # case that would mean that num is not prime
                if counter2 == counter1-1:
                    return False
                else:
                    # increment counter2 
                    counter2 += 1
                    # update v
                    modNum = (modNum**2)%num 
        trial -= 1
    # if none of these conditions have been met, num is likely tru   
    return True 

def generateLargePrime():
    """""Returns a prime number in the range from 2^1023 to (2^1024)-1"""
    while True:
        num = random.randrange(2**(1023), 2**(1024)-1)
        if isPrime(num):
            return num

def padHash(hashNum,size):
    """Pads all inputs until its the size of size bits"""
    hashLength = len(bin(hashNum)[2:])
    if (hashLength!=size):
        paddedHash = '0'*(size-hashLength)
        paddedHash = paddedHash + bin(int(hashNum))[2:]
    else:
        paddedHash = bin(int(hashNum))[2:]
    return paddedHash

def padOAEP(message):
    # Set the messge to 768 bits because the modulus we generated in 
    # the generateLargePrime() function is 1024 bits, so our message
    # is covered for exactly 768 bits.
    message = message + (768 - len(message))*'0'
    lenK0 = 128
    lenK1 = 128
    # Set r to be a random value between 2^127 and 2^128
    r = 198010546117653878157931265461103217903#random.randrange(2**127,2**128)
    # Add K1 zeroes to the back of our message
    message = int(message,2) << lenK1

    # Use hash function from imported Crypto.hash library to expand r.
    # We need r to be 896 bits so we will actually hash it 4 times
    hashlist = []
    hash1 = SHA256.new()
    hash1.update(bin(r)[2:])
    hash1 = int(hash1.hexdigest(),16)
    # Pad to 256 bits before putting in array
    hashlist.append(padHash(hash1,256))
    hash2 = SHA256.new()
    hash2.update(bin(r+1)[2:])
    hash2 = int(hash2.hexdigest(),16)
    # Pad to 256 bits before putting in array
    hashlist.append(padHash(hash2,256))
    hash3 = SHA256.new()
    hash3.update(bin(r+2)[2:])
    hash3 = int(hash3.hexdigest(),16)
    # Pad to 256 bits before putting in array
    hashlist.append(padHash(hash3,256))
    hash4 = SHA256.new()
    hash4.update(bin(r+3)[2:])
    # Shift our last hash to the right by 128 to get to 896
    hash4 = int(hash4.hexdigest(),16) >> 128
    # Pad to 256 bits before putting in array
    hash4 = padHash(hash4,256)
    # Shift to the right by 128 bits
    hash4 = int(hash4,2) >> 128
    # And pad to 128 bits
    hash4 = padHash(hash4,128)
    # Now, append hash4
    hashlist.append(hash4)
    G = ''
    # Compile all of the hashes into string variable G
    for h in hashlist:
        G += h
    # XOR message and G
    output1 = message ^ int(G,2)
    output1 = padHash(output1,896)
    if type(output1) != str:
        output1 = bin(output1)[2:]
    # Reduce output1 to K0 bits 
    hash5 = SHA256.new()
    hash5.update(output1)
    hash5 = int(hash5.hexdigest(),16)
    HOfOutput1 = hash5 >> 128 # Get rid of last 128 bits to get to 128 bits instead of 256 bits

    output2 = HOfOutput1 ^ r
    output2 = padHash(output2,128)
    if type(output2) != str:
        output2 = bin(output2)[2:]
    return (output1 + output2)

def unpadOAEP(paddedMessage):
    # Split paddedMessage after first 896 bits
    a = paddedMessage[:896]
    b = paddedMessage[896:]
    Hash = SHA256.new()
    Hash.update(a)
    HashOfa = int(Hash.hexdigest(),16) >> 128
    # Get back the random string using XOR
    r = int(b,2) ^ HashOfa

    hashlist = []
    hash1 = SHA256.new()
    hash1.update(bin(r)[2:])
    hash1 = int(hash1.hexdigest(),16)
    # Pad to 256 bits then append to array
    hashlist.append(padHash(hash1,256))
    hash2 = SHA256.new()
    hash2.update(bin(r+1)[2:])
    hash2 = int(hash2.hexdigest(),16)
    # Pad to 256 bits then append to array
    hashlist.append(padHash(hash2,256))
    hash3 = SHA256.new()
    hash3.update(bin(r+2)[2:])
    hash3 = int(hash3.hexdigest(),16)
    # Pad to 256 bits then append to array
    hashlist.append(padHash(hash3,256))
    hash4 = SHA256.new()
    hash4.update(bin(r+3)[2:])
    # Shift our last hash to the right by 128 to get to 896
    hash4 = int(hash4.hexdigest(),16) >> 128
    # Pad to 256 bits before putting in array
    hash4 = padHash(hash4,256)
    # Shift to the right by 128 bits
    hash4 = int(hash4,2) >> 128
    hash4 = bin(hash4)[2:]
    # And pad to 128 bits
    paddedHash4 = ''
    if len(hash4) != 128:
        paddedHash4 += '0'*(128 - len(hash4))
        paddedHash4 += hash4
    # Now, append hash4
    hashlist.append(paddedHash4)
    G = ''
    # Compile all of the hashes into string variable G
    for h in hashlist:
        G += h
    # Decoded message is message||K1
    decodedMessage = int(a,2) ^ int(G,2)
    decodedMessage = decodedMessage >> 128
    """
    # Convert decodedMesage to a number of base 10
    decodedMessage = int(bin(decodedMessage)[2:],2)
    # Convert decodedMessage to a string and return
    return intToString(decodedMessage)
    """
    return bin(decodedMessage)[2:]

def encrypt(message,n,totient,e):
    """Returns an encrypted form of the unencrypted message input"""
    # The inverse of k mod totient is our private key. Store in d
    d = modularInverse(e,totient) 
    # message^e mod n is our encrypted message. Store in encryptedMsg
    encryptedMsg = pow(int(message,2),e,n) 
    # Write new text file titled "publicKey"
    pubf = open("publicKey.txt",'w+') #
    pubf.write(str(n)) # Note: the totient and n values, are both referred to as public keys, but because only the n
                        # value is used to decrypt the message later on, this will be our only public key
    pubf.close()
    # Write new text file titled "privateKey"
    privf = open("privateKey.txt",'w+')
    privf.write(str(d))
    privf.close()
    return encryptedMsg

def decrypt(encryptedMsg,publickey,privateKey):
    """Returns the decrypted form of the encrypeted message input"""
    # The decrypted message is equal to (encryptedMsg^privatekey) mod publicKey
    decryptedMsg = pow(int(encryptedMsg),int(privateKey),int(publicKey))
    # Convert decrypted output to a string of alpha/numeric characters and return
    return decryptedMsg

def pad_to_1024(b):
    bits = ''
    rest = 1024 - len(b)
    bits += '0'*rest
    bits += str(b)
    return bits

def pad_bits(b):
    bits = ''
    if len(b) % 8 != 0:
        bits += '0'*(8 - (len(b) % 8))
        bits += str(b)
    return bits

if __name__ == '__main__':
    R1 = raw_input("Would you like to encrypt or decrypt a message? ")
    # Keep asking for input until one the key words indicating encrypt or decrypt has been entered
    while (R1 not in {"Encrypt","encrypt","Decrypt","decrypt"}):
        R1 = raw_input("Please enter one of the key words 'encrypt' or 'decrypt': ")
    R2Text = raw_input("Enter the name of the text file containing your message to be encrypted or decrypted: ")
    with open(R2Text,'r') as file1:
        R2 = file1.read()
    # Generate two large primes
    p = generateLargePrime()
    q = generateLargePrime()
    # Store product of two large primes in n 
    n = p*q
    # Calculate totient
    totient = (p-1)*(q-1)
    e = 65537 # Can use 65537 as our default value for k (our public key), unless k is
              # a factor of the totient
    # In the rare case when 65537 is not a unit of the totient, 
    # pick two new random numbers and calculate a new totient. 
    # Keep generating two random numbers until a unit of the the
    # totient is found. 
    while ((e%totient)==0): 
        p = generateLargePrime()
        q = generateLargePrime()
        n = p*q
        totient = (p-1)*(q-1)
    # Case when user wants to encrypt list
    if R1 in {"Encrypt","encrypt"}:
        # elist will be the text file containing the encrypted list of passcodes we will write to
        elist = open("encryptedMessage.txt",'w+')
        # Check to see if message is less than 768 bits, which is max size that can be encrypted  
        # with key size of 1024.
        while (len(stringToBitList(R2)) > 768):
            print "This message is too long to encrypt! Must pick a new message"
            R2Text = raw_input("Enter the name  of a text file containing your valid sized message (must be less than 768 bits): ")
            with open(R2Text,'r') as listf:
                R2 = listf.read()
        # Convert input to binary string and use OAE padding to pad message
        paddedMessage = padOAEP(bitListToBinString(stringToBitList((R2))))
        # Use RSA encryption to encrypt padded message
        encryptedMessage = encrypt(paddedMessage,n,totient,e)
        # Write padded and then encrypted message to text file
        elist.write(str(encryptedMessage))
        print ("Please find a file named encryptedMessage.txt containing your encrypted message, " +
            "a file named publicKey.txt containing your public key which may be stored anywhere " + 
            "and a file named privateKey.txt which must be stored safely")
        
    # Case when user wants to decrypt list
    elif R1 in {"Decrypt","decrypt"}:
        # Access the value of the public key
        publicText = raw_input("Enter the name of a the text file containing the public key: ")
        with open(publicText,'r') as pub:
            publicKey = pub.read()
        # Access the value of the private key
        privateText = raw_input("Enter the name of the text file containing private key: ")
        with open(privateText,'r') as pri:
            privateKey = pri.read()
        dlist = open("decryptedMessage.txt",'w+')
        # Use RSA to decrypt message
        decryptedMessage = decrypt(R2,int(publicKey),int(privateKey))
        decryptedMessage = bin(decryptedMessage)[2:]
        # Convert decryptedMessage to a binary string and use OAE padding to depad message
        unpaddedMessage = unpadOAEP(pad_to_1024(decryptedMessage))
        # Write depadded and decrypted message as a string to text file
        dlist.write(intToString(int(unpaddedMessage,2)))
        print ("Please find a file named decryptedMessage.txt containing your decrypted mesaage")










