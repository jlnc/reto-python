# Mejora del reto-10


### Conjuntos inmutables (frozenset)

 - El tipo `set` es mutable por que permite añadir y eliminar elementos al conjunto y eso no es lo que define a un conjunto desde el punto de vista matemático que se caracteriza justo por lo contrario: cuando dos conjuntos tienen elementos diferentes, entonces son conjuntos diferentes. Lo que define a un conjunto son sus elementos.
 - Esto hace que un objeto de tipo `set` no sea _hashable_ y por lo tanto no puede ser una _key_ de un diccionario.
 - En Python el tipo que más se parece a los conjuntos tal y como los conocemos en las matemáticas es el `frozenset` que es inmutable por que no permite añadir o suprimir elementos al igual que ocurre con el tipo `tuple`. Si además todos sus elementos son objetos inmutables, entonces un `frozenset` es _hashable_.
 - La principal ventaja que aporta el tipo `frozenset` respecto al tipo `tuple` son las operaciones propias de los conjuntos.
 - En la clase `InstagramImage`, la constante `_FILTROS` es un diccionario cuyas _keys_ son conjuntos (`frozenset`) con los nombres de los filtros de un módulo dado y cuyos valores son el módulo que proporciona dichos filtros:

```python
    _FILTROS: dict[frozenset[str], str] = {
        frozenset(pilgram.__all__[1:]): "pilgram",
        frozenset(pilgram.css.__all__): "pilgram.css",
        }
```

 - Un ejemplo del uso de las operaciones con conjuntos es el método de clase `filtros` que usa la unión de conjuntos para obtener un único iterable con todos los filtros que proporcionan tanto `pilgram` como `pilgram.css`:

```python
    @classmethod
    def filtros(cls):
        return reduce(set.union, cls._FILTROS, set())
```

 - Usando este método es trivial escribir el bucle que permite calcular el nombre de la función que usaremos para aplicar el filtro:

```python
        if filtro in self.filtros():
            for fset, modulo in InstagramImage._FILTROS.items():
                if filtro in fset:
                    break
            self.__filter = eval(f"{modulo}.{filtro}")
```

En el caso de utilizar tuplas en lugar de conjuntos, tendríamos que añadir código para el caso en que _filtro_ no se encuentre entre los valores válidos:

```python
        modulo = None
        for fset, modulo in InstagramImage._FILTROS.items():
            if filtro in fset:
                break
        if modulo is not None:
            self.__filter = f"{modulo}.{filtro}"
```

----

### Eval.


La forma segura de usar `eval` en Python es usando el módulo `ast` con la función `ast.literal_eval` que solo acepta tipos básicos, pero en este caso necesitamos usar `eval` para definir la función que aplica el filtro:
```python
            self.__filter = eval(f"{modulo}.{filtro}")
```
y con `ast.literal_eval` no es posible.

Ver [The pitfall of eval function and its safe alternative in Python.](https://eulertech.wordpress.com/2018/06/10/the-pitfall-of-eval-function-and-its-safe-alternative-in-python/).

----
