# UFV CTF 2022

## **Andrés de la Hoz Camiroaga** 
### WriteUp & WalkTrhough

###### All rights reserved &copy;<br />
---
&nbsp;  
#### MISCELLANEOUS -- **INSANE**  
&nbsp;  
El reto nos presenta un archivo comprimido `ff78cee4b6a5e0bd60e795ad8ff4f3b3.zip`  

![zip_file](https://github.com/1ocho3/ufv_CTF/blob/main/readme_required/ff78cee4b6a5e0bd60e795ad8ff4f3b3.png?raw=true)

Si tratamos de abrir el fichero, podemos observar un patrón de relación con los retos de miscelánea anteriores. Un fichero `.zip` con nombres aleatorios, protegidos con contraseña, y que se suceden el uno al otro.

![nombres_aleatorios](https://github.com/1ocho3/ufv_CTF/blob/main/readme_required/sucesi%C3%B3n_nombres-aleatorios.png?raw=true)

Si has probado a trastear con las contraseñas, ya te habrás topado con la característica principal de este reto.  
A diferencia del resto, las contraseñas de estos ficheros no siguen un patrón determinado, por lo que tomarán un valor aleatorio dentro del diccionario de contraseñas [passwords-UFV-CTF.txt](https://github.com/1ocho3/ufv_CTF/blob/70c4422e184d3d762c7819227740e044a48baa4a/files/passwords-UFV-CTF.txt)  

El reto nos anima a usar las herramientas: `JohnTheRipper` y `zip2john` para obtener las contraseñas.

Nos encontramos ante otro reto de programación.

Lo resolveremos usando `Python3` y la librería `os` para introducir conmandos en el terminal.

Antes de empezar te recomiendo que trates de analizar con perspectiva el objetivo y el camino para llegar hasta él. Sabemos lo que tenemos que hacer, y qué es lo que hay que conseguir... ¿Pero cómo vamos a llegar hasta ello?
Necesitamos automatizar la ejecución del proceso de crackeo de contraseña y descompresión del archivo.

Lo primero que haremos será crear nuestro `work-enviroment`. Crea una carpeta donde tengas todos los archivos necesarios: `ff78cee4b6a5e0bd60e795ad8ff4f3b3.zip`, [passwords-UFV-CTF.txt](https://github.com/1ocho3/ufv_CTF/blob/70c4422e184d3d762c7819227740e044a48baa4a/files/passwords-UFV-CTF.txt), y tu `scrypt.py` que llamaremos [unzip_cracker.py](https://github.com/1ocho3/ufv_CTF/blob/70c4422e184d3d762c7819227740e044a48baa4a/files/unzip_cracker.py)  

![work_enviroment](https://github.com/1ocho3/ufv_CTF/blob/main/readme_required/work-envirioment.png?raw=true)
