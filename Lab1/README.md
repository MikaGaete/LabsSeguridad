# Laboratorio 1: Introducción a la Seguridad Computacional

### Mikael Gaete - Dylan Riquelme

---

## Análisis Exploratorio

### a) Pruebe los servicios con distintos tipos de entrada.

Para testear el servicio A, se generó un [script](https://github.com/MikaGaete/LabsSeguridad/blob/main/Lab1/parte_a.py) el cual envía un string compuesto por ceros cuyo
largo varía desde el string vacío a un string de largo 72. Esto con el fin de determinar que el tamaño de los 
bloques corresponde a los 16 bytes esperados.

Con respecto a como se modificaba el largo de los mensajes de respuesta con respecto al cambio de largo de inputs, 
notamos que el primer bloque generado es con 8 bytes del input y del segundo en adelante son 16 bytes. Esto se 
observa cuando se envía el mensaje `'0' * 8` y en respuesta se genera mensaje encriptado de largo menor que `'0' * 9`. 
Sin embargo, el largo anterior no cambia hasta que se envía el mensaje `'0' * 24`, dando a entender que el largo de este
primer bloque de output es menor por el IV.

Otro comportamiento que se pudo observar consiste en que, para un mismo mensaje enviado en instancias distintas, se 
genera un texto cifrado diferente lo que sugiere que las respuesta se forman de manera pseudo-aleatoria. A 
continuación se puede observar el resultado de enviar el input `'0'` en dos iteraciones distintas:

#### Cifrado retornado en el primer envio:
``` plain text
bba9aafcb41b989d421cabcef476ea7069623c7986ed6338fffc2ba32e8c2e2a3138a1a71d88b7925bcba8c94e1d4986a47b7fd4a3e2934d6dbd943d1ade74737909473be2de145ff6e4ee85cd71302039d6a07528aedc716ea869ffcbd054a4e9f30c63f67f77be778de9941e86ee28
```

#### Cifrado retornado en el segundo envío:
``` plain text
f3dd9b0fbbec9158cf8a50de422e652e1636bc9fa047371d97bc7dd52fbd0980be53b5edd378c4ccf630e345aaccbf919473602f4bbf9fec79c70477cfab74e33682cc48d639635c9f46b0809bb43e0cfedaf42b55dc0a4dfb605e2eb236a442e432c34e9647aff96d3cfc6412386cd3"
```

Para el testear el servicio B, probamos desencriptando los dos mensajes cifrados resultantes del envío del string `'0'` 
mencionado anteriormente, a partir de esto pudimos determinar que el servidor desencripta correctamente los mensajes. 
Además, si se elimina el último caracter de alguno de los mensajes cifrados y se envía al servidor nos retorna el 
siguiente error: `"hex: encoding/hex: odd length hex string"`. Si en vez de eliminarlo, lo cambiamos por un valor 
distinto, se nos retorna el error `"pkcs7: invalid padding (last byte does not match padding)"`

### b) Cree un programa basado en el código base que envía un mensaje 𝑚 al servidor A y le envía la respuesta del servidor A al servidor B.

Para llevar a cabo el siguiente punto se generó el siguiente [script](https://github.com/MikaGaete/LabsSeguridad/blob/main/Lab1/parte_b.py) el cual es una versión modificada 
del script utilizado en la parte a) la cual no realiza tantas iteraciones y que imprime el mensaje enviado, la 
codificación recibida y la decodificación recibida. Esto nos permitió observar nuevamente cuadno ocurren los saltos 
de bloque y la manera en la que el servidor retorna la información, la cual en este caso corresponde a caracteres 
hexadecimales.

### c) ¿Cómo podría conocer en un contexto genérico, el tamaño del bloque utilizado por el cifrador, sin conocer el cifrador?

Para esto se podría utilizar el mismo ejercicio antes mencionado:
1. Variar el largo de los inputs.
2. Observar cuando se generan _saltos_ en el largo de los bloques. 
3. Determinar el tamaño del bloque en base a la cantidad de caracteres que tenía el mensaje enviado en cada salto.

---

## Ejecución del ataque Padding Oracle

### d) Cree una función que permita descifrar el último carácter del texto cifrado.

La función creada se puede encontrar en el siguiente [script](https://github.com/MikaGaete/LabsSeguridad/blob/main/Lab1/parte_d.py).

### e) Modifique la función anterior para descifrar un bloque completo.

La función creada se puede encontrar en el siguiente [script](https://github.com/MikaGaete/LabsSeguridad/blob/main/Lab1/parte_e.py).

### f) Ejecute satisfactoriamente el ataque descrito para obtener _key_.

La función creada se puede encontrar en el siguiente [script](https://github.com/MikaGaete/LabsSeguridad/blob/main/Lab1/parte_f.py),
al hacer uso de ésta se obtiene el siguiente texto plano:

``` plain text
4a16390020"}\x04\x04\x04\x04b1fe6ce7bf54d32c6342c62a1797cd87bf74f04b841b9c18"secret":"83c804{"name":"aaaaa",Y\xdf\xcb\xcf"t\xa6\xc2\x19V\x8c\x0c\xa1C\xba\xf7
```

El cual al reordenarlo se obtiene lo siguiente:

``` plain text
Y\xdf\xcb\xcf"t\xa6\xc2\x19V\x8c\x0c\xa1C\xba\xf7{"name":"aaaaa","secret":"83c804bf74f04b841b9c186342c62a1797cd87b1fe6ce7bf54d32c4a16390020"}\x04\x04\x04\x04
```

Lo que nos muestra claramente que el mensaje enviado fue `'aaaaa'` y que la _key_ utilizada es 
`'83c804bf74f04b841b9c186342c62a1797cd87b1fe6ce7bf54d32c4a16390020'`.