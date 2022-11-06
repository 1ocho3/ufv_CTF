# UFV CTF 2022

## by: **Uno.Ocho.Tres !.8.3** 
### WriteUp & WalkTrhough

###### All rights reserved &copy;<br />
---
&nbsp;  
#### MISCELLANEOUS -- **INSANE**  
&nbsp;  
El reto nos presenta un archivo comprimido [`ff78cee4b6a5e0bd60e795ad8ff4f3b3.zip`](https://github.com/1ocho3/ufv_CTF/blob/15b6f1eb908a6023000a8efbb9e619e964de6656/miscellaneous/insane/files/ff78cee4b6a5e0bd60e795ad8ff4f3b3.zip)  

![zip_file](https://github.com/1ocho3/ufv_CTF/blob/main/miscellaneous/insane/readme_required/ff78cee4b6a5e0bd60e795ad8ff4f3b3.png?raw=true)

Si tratamos de abrir el fichero, podemos observar un patrón de relación con los retos de miscelánea anteriores. Un fichero `.zip` con nombres aleatorios, protegidos con contraseña, y que se suceden el uno al otro.

![nombres_aleatorios](https://github.com/1ocho3/ufv_CTF/blob/main/miscellaneous/insane/readme_required/sucesi%C3%B3n_nombres-aleatorios.png?raw=true)

Si has probado a trastear con las contraseñas, ya te habrás topado con la característica principal de este reto.  
A diferencia del resto, las contraseñas de estos ficheros no siguen un patrón determinado, por lo que tomarán un valor aleatorio dentro del diccionario de contraseñas [passwords-UFV-CTF.txt](https://github.com/1ocho3/ufv_CTF/blob/774c1faa27fdf86332161faf372dd477996d30e5/miscellaneous/insane/files/passwords-UFV-CTF.txt)  

El reto nos anima a usar las herramientas: `JohnTheRipper` y `zip2john` para obtener las contraseñas.

Nos encontramos ante otro reto de programación.

Lo resolveremos usando `Python3` y la librería `os` para introducir conmandos en el terminal.

<p align="justify">Antes de empezar te recomiendo que trates de analizar con perspectiva el objetivo y el camino para llegar hasta él. Sabemos lo que tenemos que hacer, y qué es lo que hay que conseguir... ¿Pero cómo vamos a llegar hasta ello?
Necesitamos automatizar la ejecución del proceso de crackeo de contraseña y descompresión del archivo.</p>


Lo primero que haremos será crear nuestro `work-enviroment`. Crea una carpeta donde tengas todos los archivos necesarios: `ff78cee4b6a5e0bd60e795ad8ff4f3b3.zip`, [passwords-UFV-CTF.txt](https://github.com/1ocho3/ufv_CTF/blob/774c1faa27fdf86332161faf372dd477996d30e5/miscellaneous/insane/files/passwords-UFV-CTF.txt), y tu `scrypt.py` que llamaremos [`unzip_cracker.py`](https://github.com/1ocho3/ufv_CTF/blob/a91f018f715c8cc976542391da955a4b4dd8a132/miscellaneous/insane/files/unzip_cracker.py)  

![work_enviroment](https://github.com/1ocho3/ufv_CTF/blob/main/miscellaneous/insane/readme_required/work-envirioment.png?raw=true)  

El código resulta una secuencia sencilla de comandos que deben ser repetidos en un bucle semi-infinito. ¿Qué quiere decir esto? Puedes forzar un bucle infinito, o cuasi-infinito, que terminará inevitablemente cuando se llegue a descomprimir el último archivo y tu scrypt trate de descomprimir `flag.txt`. En cuyo caso dará error, y finalizará. Es una forma de acerlerar tu avance en el CTF pero si lo deseas puedes no ahorrarte este paso y añadir que el programa termine cuando aparezca el archivo `flag.txt` y lo imprima por pantalla. Veremos como añadir esta opción a tu código.

Lo primero es crear la clase `unzip_cracker` desde la que crearemos los metodos para resolver el reto.  
En el método constructor introducimos todos los nombres conocidos de los archivos que necesitaremos.
```python
if __name__=='__main__':
    import os
    class unzip_cracker:
        def __init__(self):
            self.h='hash'
            self.crk='crackeado.txt'
            self.scrp='unzip_cracker.py'
            self.psswd='passwords-UFV-CTF.txt'
```

Para conseguir el nombre del archivo es tan fácil como sacar una lista con los nombres de nuestro directorio y eliminar los nombres conocidos.
```python
        def file_name(self):
            files=os.listdir()
            files.remove(self.scrp)
            files.remove(self.psswd)
            return files[0]
```
Te habrás dado cuenta, de que no hemos eliminado `self.h` ni `self.crk` de la lista `files`. Esto es, porque más adelante, eliminaremos estos archivos inmediatamente después de crearlos y obtener la información que nos interesa.  

Siguiente paso. JohnTheRipper necesita un 'intérprete' que exprese los archivos `.zip` en un formato legible para john, esto se hace con `zip2john` de la siguiente forma:

```Brainfuck
zip2john file.zip > hash
``` 
Que expresado en nuestro scrypt queda así:

```python
os.system('clear')
os.system(f'zip2john {self.file_name()} > {self.h}')
```
Una vez sacado el hash debemos crackearlo con nuestro diccionario. En el terminal se ejecuta de la siguiente forma:

```Brainfuck
john hash --wordlist=passwords-UFV-CTF.txt > crackeado.txt
```

Representado en python así:

```python
os.system(f'john {self.h} --wordlist={self.psswd} > {self.crk}')
os.system(f'rm {self.h}')#hash ya no sirve ningún propósito
```
Ahora queda aislar la contraseña que se encuentra en crackeado.txt con un sencillo protocolo de lectura de fichero, eliminación de lineas y separación por espacios.

```python
f=open(self.crk,'r')
lines=f.readlines()
lines.pop(0)
ps=lines[0].split(' ')
f.close()
os.system(f'rm {self.crk}')#En este punto ya no sirve propósito 
return ps[0]
```

Gráficamente esto es lo que estamos realizando en el contenido de `crackeado.txt`:

```
Loaded 1 password hash (PKZIP [32/64])
11111111         (ff78cee4b6a5e0bd60e795ad8ff4f3b3.zip/0c959fe7360c400b8cf81225dc323a4d.zip) 

----------------------- #Eliminamos la primera línea
11111111         (ff78cee4b6a5e0bd60e795ad8ff4f3b3.zip/0c959fe7360c400b8cf81225dc323a4d.zip)

----------------------- #Separamos por espacios

['11111111', '', '', '', '', '', '', '', '', '(ff78cee4b6a5e0bd60e795ad8ff4f3b3.zip/0c959fe7360c400b8cf81225dc323a4d.zip)']

----------------------- #Devolvemos el primer elemento que será nuestra contraseña
11111111
```
Con lo que nuestra función `crackear`, aunando todo, resulta en el siguiente método:
```python
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
```
###### `rm /root/.john/john.pot` elimina el historial de john. Al trabajar repetidamente con archivos con el mismo nombre, john puede dar problemas.  

Solo queda descomprimir el archivo con la contraseña que ya conocemos.
Para especficar una contraseña, `unzip` requiere el parámetro `-P`:
```Brainfuck
unzip -P V3ryStr0ngP4ssw0rd_1 comprimido.zip
```  
Lo traducimos a python:
```python
os.system(f'mv {self.file_name()} comprimido.zip') #Modifica el nombre aleatorio del archivo, por uno conocido, para evitar complicaciones con el método file_name().
os.system(f'unzip -P {self.crackear()} comprimido.zip') #Descomprime el archivo con la última contraseña crackeada.
```  
En este punto el script está terminado y finalizaría al producirse un error cuando se descomprimiese el último `.zip,` y `flag.txt` haya sido extraido del `.zip` 
Pero por la estrucutra de nuestro scrypt, `flag.txt` se modificaría y pasaría a llamarse `comprimido.zip`. Esto se bypasea haciendo un simple `cat` sobre `comprimido.zip` ya que por mucho `.zip` que tenga, es un mero `.txt`, el cat sobre nuestro falso zip nos daría la flag.  

![false_zip_file](https://github.com/1ocho3/ufv_CTF/blob/main/miscellaneous/insane/readme_required/false_zip_file.png?raw=true)  

Para evitar esto podemos poner el broche de oro y automatizar también, la detección de `flag.txt`, y su muestreo en pantalla.
```python
flag='flag.txt'
lista=os.listdir() #Saca todos los nombres de nuestros archivos
if flag in lista: #Si flag.txt existe, abre el archivo, lo lee, lo muestra y acaba el programa.
    f=open('flag.txt','r')
    print(f.readlines())
    f.close()
    os.system(f'rm comprimido.zip')
    exit()

else:
    os.system(f'rm comprimido.zip')
```
Por último añade un bucle infinito e instancia la clase y ejecuta el método run:
```python
def run(self):
    while True:
    self.unzip()

scrypt=unzip_cracker()
scrypt.run()
```
En conjunto, todo el scrypt [`unzip_cracker.py`](https://github.com/1ocho3/ufv_CTF/blob/a91f018f715c8cc976542391da955a4b4dd8a132/miscellaneous/insane/files/unzip_cracker.py) queda de la siguiente forma:
```python
if __name__=='__main__':
    import os
    class unzip_cracker:
        def __init__(self):
            self.h='hash'
            self.crk='crackeado.txt'
            self.scrp='unzip_cracker.py'
            self.psswd='passwords-UFV-CTF.txt'

        def file_name(self):
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
```  
A crackear!!!  Recuerda introducir tu `wordlist`, tu archivo `.zip` y el scrypt [`unzip_cracker.py`](https://github.com/1ocho3/ufv_CTF/blob/a91f018f715c8cc976542391da955a4b4dd8a132/miscellaneous/insane/files/unzip_cracker.py) en una misma carpeta, y ejecuta!

![SUCCESS](https://github.com/1ocho3/ufv_CTF/blob/main/miscellaneous/insane/readme_required/SUCCESS.gif?raw=true) 

&nbsp;
![FLAG.TXT](https://github.com/1ocho3/ufv_CTF/blob/main/miscellaneous/insane/readme_required/flag_txt.png?raw=true)

Gracias


## _**!.8.3**_
