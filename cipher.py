import json
from string import ascii_lowercase
import sys


class Cipher:
    def __init__(self, steckerbrett={" ": " "}, setting=None, alpha=0, beta=0, gamma=0):
        self.steckerbrett = steckerbrett
        self.alphabet = list(ascii_lowercase)
        self.alpha=alpha
        self.beta=beta
        self.gamma=gamma
        if setting != None:
            try:
                self.setting = json.load(open(setting, 'r'))[0]
            except IOError as e:
                print("Error: No Such Setting file " + e)
            finally:
                self.steckerbrett = self.setting['steckerbrett']
                self.alpha = self.setting['alp']
                self.beta = self.setting['bet']
                self.gamma = self.setting['gam']

        elif alpha != None and beta != None and gamma != None and steckerbrett != None:
            if type(steckerbrett) is not dict:
                self.steckerbrett = {" ": " "}
            self.alpha = alpha
            self.beta = beta
            self.gamma = gamma

        else:
            if type(steckerbrett) is not dict:
                self.steckerbrett = {" ": " "}
            pos_rotor = [self.alpha, self.beta, self.gamma]
            for rotor in pos_rotor:
                if rotor == None or type(rotor) is not int or type(rotor) is not float:
                    rotor = 0
                else:
                    rotor = rotor % 26
            self.alpha=pos_rotor[0]
            self.beta=pos_rotor[1]
            self.gamma=pos_rotor[2]

        for letter in list(self.steckerbrett.keys()):
            if letter in self.alphabet:
                self.alphabet.remove(letter)
                self.alphabet.remove(self.steckerbrett[letter])
                self.steckerbrett.update({self.steckerbrett[letter]:letter})
        
        self.reflector=[revlet for revlet in reversed(self.alphabet)]

    def permutation(self,rotor):
        new_alphabet=''.join(self.alphabet)
        new_alphabet=list(new_alphabet)
        for iter in range(rotor):
            new_alphabet.insert(0,new_alphabet[-1])
            new_alphabet.pop(-1)
        return new_alphabet

    def inverse_permutation(self,rotor):
        new_alphabet=''.join(self.alphabet)
        new_alphabet=list(new_alphabet)
        for iter in range(rotor):
            new_alphabet.append(new_alphabet[0])
            new_alphabet.pop(0)
        print(self.alphabet)
        print(new_alphabet)
        return new_alphabet

    def encrypt_text(self,text):
        cipheredtext=[]
        text=text.lower()
        text.split()

        for letter in text:
            if letter in self.steckerbrett:
                cipheredtext.append(self.steckerbrett[letter])
                self.alpha+=1
                if self.alpha%len(self.alphabet)==0:
                    self.beta+=1
                    self.alpha=0
                if self.beta%len(self.alphabet)==0 and self.alpha%len(self.alphabet)!=0 and self.beta>=len(self.alphabet)-1:
                    self.gamma+=1
                    self.beta=self.beta-len(self.alphabet)
            else:
                temp_letter=self.permutation(self.alpha)[self.alphabet.index(letter)]
                print("Alpha={}".format(temp_letter))
                temp_letter=self.permutation(self.beta)[self.alphabet.index(temp_letter)]
                print("Beta={}".format(temp_letter))
                temp_letter=self.permutation(self.gamma)[self.alphabet.index(temp_letter)]
                print("Gamma={}".format(temp_letter))

                temp_letter=self.reflector[self.alphabet.index(temp_letter)]
                print("Reflector={}".format(temp_letter))

                temp_letter=self.inverse_permutation(self.gamma)[self.alphabet.index(temp_letter)]
                print("Gamma={}".format(temp_letter))
                temp_letter=self.inverse_permutation(self.beta)[self.alphabet.index(temp_letter)]
                print("Beta={}".format(temp_letter))
                temp_letter=self.inverse_permutation(self.alpha)[self.alphabet.index(temp_letter)]
                print("Alpha={}".format(temp_letter))

                cipheredtext.append(temp_letter)
                print(temp_letter)
                self.alpha+=1
                if self.beta%len(self.alphabet)==0 and self.alpha%len(self.alphabet)!=0 and self.beta>=len(self.alphabet)-1:
                    self.gamma+=1
                    self.beta=self.beta-len(self.alphabet)
                print("Alpha={}".format(self.alpha))

        return ''.join(cipheredtext)

    def encryptor(self,file):
        try:
            file=open(file,'r')

        except IOError as e:
            print("Enigma Error: No File to Encrypt")
            return None
        finally:
            encrypted_file=open("output.txt",'w')
            for line in file:
                encrypted_file.write(self.encrypt_text(line.rstrip())+'\n')
            file.close()
            encrypted_file.close()          

if __name__ == "__main__":
    file=sys.argv[1]
    cy=Cipher()
    cy.encryptor(file)
