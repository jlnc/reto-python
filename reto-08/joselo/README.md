# Reto 08: mejoras


Cuatro implementaciones diferentes de la clase `ResizeImage`:

 1. La más básica, atributos públicos de lectura/escritura.

 2. Con atributos "privados" con acceso de solo lectura.

 3. Una `dataclass` con atributos de lectura/escritura y posibilidad de dar el tamaño de la imágen de tres maneras.

 4. Una `dataclass` "frozen" pero renunciando a la sobrecarga.

----
----
## Chequeos incorrectos.
#### O lo que ocurre cuando crees que las cosas funcionan pero no lo compruebas.
 -------------------------------------------------------
En el método `check` compruebo cosas como el tamaño de la imágen, la existencia del fichero `filein` o el mimetype; para ello utilizo, ingenuamente, tests separados como
```python
        if not self.filein.is_file():
            raise FileNotFoundError(f"No encuentro el fichero {self.filein}")
```
para no intentar leer un fichero que no existe, o
```python
        if os.path.getsize(self.filein) == 0:
            raise ValueError(f"El fichero {self.filein} está vacio.")

```
para no intentar leer un fichero vacío.

Se puede comprobar que el fichero `filein` es una imágen de dos maneras, la primera es comprobando el mimetype con el módulo `mimetypes`:
```python
import mimetypes

    ...

mimetypes.init()

    ...

        mimetype = mimetypes.guess_type(self.filein)[0]
        if not mimetype.startswith('image'):
            raise ValueError(
                f"El fichero {self.filein} no parece una imágen.")
```
Pero esta vía tiene un defecto, el mimetype que nos entrega la función `guess_type` está basado en la extensión del nombre del fichero y no en su contenido; de hecho podemos tener un fichero vacío, creado con `touch`, o un fichero de texto plano con la extensión `.png` y `guess_type` nos dirá que el mimetype es _"image/png"_. O peor aún, podemos tener una imágen a la que se le añada la extensión _".txt"_ y `guess_type` nos dirá que es _"text/plain"_

Está claro que este método no nos vale.

Otra forma es obtener el mimetipe de los metadatos del fichero a los que podemos acceder con la clase `Image` del módulo `wand.image` _(con la libería `PIL` sería parecido)_
```python
        im = Image(filename=self.filein)
        if not im.mimetype.startswith("image"):
            raise ValueError(
                f"El fichero {self.filein} no parece una imágen.")
```
Sería perfecto si no fuera por que al leer el fichero `Wand` genera sus propias excepciones; y entre ellas están:

 - **BlobError** que se genera al intentar leer un fichero que no existe.
 
 - **MissingDelegateError** que se genera cuando intentamos leer un fichero con una extensión ajena al mundo de las imágenes tales como _'.sqlite'_, _'.pgn'_,...
 
 - **CorruptImageError** que se genera cuando intentamos leer un fichero vacío o un fichero de texto plano.

Hay muchas otras excepciones que se generan por diversas circunstancias y no es práctico consideralas una a una, por eso lo mejor es tratar algunas por separado con los métodos habituales para poder obtener información del problema y tratar el resto de la forma más general posible:
```python
        if not self.filein.is_file():
            raise FileNotFoundError(f"No encuentro el fichero {self.filein}")

        if os.path.getsize(self.filein) == 0:
            raise ValueError(f"El fichero {self.filein} está vacio.")

        try:
            _ = Image(filename=self.filein)
        except Exception as e:
            raise RuntimeError(
                f"O {self.filein} no es una imágen o está corrupta.") from e
```
Por último, la lista de excepciones de `Wand`: [wand.exceptions — Errors and warnings](https://docs.wand-py.org/en/0.6.7/wand/exceptions.html)
____
