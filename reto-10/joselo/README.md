# Mejora del reto-10
----

### Conjuntos inmutables (frozenset)

El tipo `set` es mutable; permite añadir y eliminar elementos a un conjunto y eso no es lo que define a un conjunto desde el punto de vista matemático, que se caracteriza justo por lo contrario: cuando dos conjuntos tienen elementos diferentes, entonces son conjuntos diferentes. Esto hace que un objeto de tipo `set` no sea _hashable_ y por lo tanto no puede ser una _key_ de un diccionario.

En Python el tipo que más se parece a los conjuntos tal y como los conocemos en las matemáticas y que además es _hashable_, es el `frozenset` que es inmutable y es _hashable_ siempre que sus elementos sean también _hashables_ (inmutables) al igual que ocurre con el tipo `tuple`. La principal ventaja que aporta el tipo `frozenset` respecto al tipo `tuple`, es la facilidad con la que se pueden resolver ciertos problemas usando las operaciones propias de los conjuntos.

En la clase `InstagramImage`, la constante `_FILTROS` es un diccionario cuyas `keys` son conjuntos (`frozenset`) con los nombres de los filtros de un módulo dado y cuyos valores son el módulo que proporciona dichos filtros:

```python
    _FILTROS: dict[frozenset[str], str] = {
        frozenset(
            ["_1977", "aden", "brannan", "brooklyn", "clarendon", "earlybird",
             "gingham", "hudson", "inkwell", "kelvin", "lark", "lofi",
             "maven", "mayfair", "moon", "nashville", "perpetua", "reyes",
             "rise", "slumber", "stinson", "toaster", "valencia", "walden",
             "willow", "xpro2"]
            ): "pilgram",
        frozenset(
            ["contrast", "grayscale", "hue_rotate", "saturate", "sepia"]
            ): "pilgram.css",
        }
```

Un ejemplo de las ventajas que menciono en el párrafo de arriba es el método de clase `filtros` que usa la unión de conjuntos para obtener un único iterable con todos los filtros que proporcionan tanto `pilgram` como `pilgram.css`:

```python
    @classmethod
    def filtros(cls):
        """La unión de todos los subconjuntos de filtros."""
        return reduce(set.union, cls._FILTROS, set())
```

Usando este método es trivial escribir el bucle que permite calcular el nombre de la función que usaremos para aplicar el filtro:

```python
        if filtro in self.filtros():
            for item in InstagramImage._FILTROS:
                if filtro in item:
                    modulo = InstagramImage._FILTROS[item]
                    break
            self.__filter = f"{modulo}.{filtro}"
```

En el caso de utilizar tuplas en lugar de conjuntos, tendríamos que añadir código para el caso en que _filtro_ no se encuentre entre los valores válidos:

```python
        modulo = None
        for item in InstagramImage._FILTROS:
            if filtro in item:
                modulo = InstagramImage._FILTROS[item]
                break
        if modulo is not None:
            self.__filter = f"{modulo}.{filtro}"
```

En este caso concreto no es una gran ventaja salvo por el método de clase que puede ser usado de forma externa para iterar el conjunto de todos los filtros que con tuplas es más laborioso de construir.

----

### Eval.

La forma segura de usar `eval` en Python es usando el módulo `ast` con la función `ast.literal_eval` aunque no se puede usar de la misma manera que `eval`. Ver [The pitfall of eval function and its safe alternative in Python.](https://eulertech.wordpress.com/2018/06/10/the-pitfall-of-eval-function-and-its-safe-alternative-in-python/)

El código de `InstagramImage.execute` podría ser de la siguiente manera:

```python
    def execute(self) -> None:
        """execute."""
        import ast
        try:
            image = Image.open(self.__filein)
            func_call = f"{self.__filter}(image)"
            image = ast.literal_eval(func_call)
            image.save(self.__fileout)
        except Exception:
            pass
```

pero no funciona. ¿Por qué?

----
