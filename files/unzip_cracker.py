if __name__=='__main__':
    import os
    class unzip_cracker:
        def __init__(self):
            self.h='hash'
            self.crk='crackeado.txt'
            self.scrp='unzip_cracker.py'
            self.psswd='passwords-UFV-CTF.txt'

        def file_name(self):
            #files=[]
            files=os.listdir()
            files.remove(self.scrp)
            files.remove(self.psswd)
            return files[0]
        
        def crackear(self):
                os.system('rm /root/.john/john.pot') #John trouble prevention
                os.system('clear')
                os.system(f'zip2john {self.file_name()} > {self.h}')
                os.system(f'john {self.h} --wordlist={self.psswd} > {self.crk}')
                os.system(f'rm {self.h}')#hash ya no sirve ningún propósito
                f=open(self.crk,'r')
                lines=f.readlines()
                lines.pop(0)
                ps=lines[0].split(' ')
                f.close()
                os.system(f'rm {self.crk}')#En este punto ya no sirve propósito 
                return ps[0]
        
        def unzip(self):
            os.system('clear')
            os.system(f'mv {self.file_name()} comprimido.zip')
            os.system(f'unzip -P {self.crackear()} comprimido.zip')
            flag='flag.txt'
            lista=os.listdir()
            if flag in lista:
                f=open('flag.txt','r')
                print(f.readlines())
                f.close()
                exit()
            else:
               os.system(f'rm comprimido.zip')            
        
        def run(self):
            while True:
                self.unzip()

    scrypt=unzip_cracker()
    scrypt.run()

