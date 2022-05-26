# Mejora del reto-10
----

### Conjuntos inmutables (frozenset)

El tipo `set` es mutable; se puede añadir y eliminar elementos a un conjunto y eso no es lo que define a un conjunto desde el punto de vista matemático, que se caracteriza justo por lo contrario: cuando dos conjuntos tienen elementos diferentes, entonces son conjuntos diferentes. Un objeto de tipo `set` no es _hashable_ y por lo tanto no puede ser una _key_ de un diccionario.

En Python el tipo que más se parece a un conjunto tal y como lo conocemos en las matemáticas y que además es _hashable_, es el `frozenset` que es inmutable y es _hashable_ siempre que sus elementos sean también _hashables_ al igual que ocurre con el tipo `tuple`. La principal diferencia entre el tipo `frozenset` y el tipo `tuple` es la facilidad con la que se pueden resolver ciertos problemas usando los conjuntos que con las tuplas son más complejos.

Un ejemplo de esto es la clase `InstagramImage` implementada de la siguiente manera.

```python
class InstagramImage:

    _FILTROS = {
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

    def __init__(self, filein: Path, fileout: Path,
                 args: Optional[dict[str, str]] = None) -> None:

        self.__filein = Path(filein)
        self.__fileout = Path(fileout)

        try:
            filtro = args['filter']
        except KeyError:
            raise

        if filtro not in self.filtros():
            raise ValueError(f"{filtro} no está en las listas de filtros.")

        FILTROS = InstagramImage._FILTROS
        modulo = [FILTROS[x] for x in FILTROS if filtro in x][0]

        self.__filter = f"{modulo}.{filtro}"

    @classmethod
    def filtros(cls):  # noqa
        return reduce(set.union, cls._FILTROS, set())
```
