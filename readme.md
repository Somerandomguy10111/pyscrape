### I: Design by contract: Guaranteeing and assuming type hint conformity

Functions
- **Arguments**: All function arguments must be type hinted.
     - Passing the correct type in arguments is **caller responsibility**:
     - Guarantee in call and assume in definition: Passsed argument conform to type hint
- **Returns**: All functions return an object that conforms to its type hint or raise an error. Note that returning and raising are mutually exclusive.
    - Returning the correct type , assuming type conformity of the passed arguments, **is callee responsbility**: 
    - Guarantee function definition and assume in function call: Returned object conforms to type hint or raises Exception
    - Functions without a type hint are implicitly assumed to return None

Classes
   - **Attributes**: All class attributes must be type hinted and conform to their type hints
   	- The __init__ method must guarantee the integrity of the type hint, assuming argument type conformity
   	- All methods manipulating attributes must guarantee type conformity
   	- All methods retrieving attributes assume the integrity of the type hints
   - **Inheritance**: Inherited attributes and methods implicitly inherit their type hints

### II: Naming

- Stick to pythonic case and spacing conventions (see also: [python-naming-convention](https://github.com/naming-convention/naming-convention-guides/tree/master/python):
  - source files: lowercase w/ snake_case, 
  - functions:  lowercase w/ snake_case; use verbs
  - classes: everything else: CamelCase; use nouns
- Function naming templates:
	- Functions that retrieve something that already exists `get_[object]` or
 	- Functions that create and then return an object `create_[object]` or`make_[object]`
- Names are searchable and distinguishable:
	- No shadowing of outer scope
	- Word trees are distinguished by prefix not suffix (e.g. plot_reference_fourier, plot_original_fourier instead of plot_fourier_reference, plot_fourier_original)
 	- Loop variables contract the list variable (e.g. instead of for number in numbers -> for n in numbers)
- Hungarian notations only used when the object appears as several types throughout the program


### III: Vertical arrangement

- **Downward dependency rule**: Arrange modules so that dependency points downward. This is also referred to as the stepdown rule.
	- For functions: Top level function first, then functions called by that function below. If lower level functions call each other, sort recursively, else sort by order of call in top level
	- For modules/files: Consider l0, l1, etc. structure to establish downward dependency of modules within directories

### IV: Size rules

- **Minimal nesting**: Max indentation level === 3 
- **Small directories**: Each dir ideally contains only 2-4 files/folders; max 5 files/folders
- **Short files**: Max ~200 loc, Ideally < 120 loc
- **Short functions**: Max ~30 loc, ideally <= 15 loc; Ideally <= 2 args, max ~ 5 args
- **Commit messges**: ~ 5 words
- **kwargs only**: Pass function arguments only by keyword

### V: Imports

- **Ordering**: First import stdlib/pypi packages, then own code arranged by how far away nearest common ancestor
- **Package inteerfaces**: Define interface of a package through __init__ file
