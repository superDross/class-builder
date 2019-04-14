# Class Builder
Quickly write class declarations in vim.

## Usage
Executing `:Class Person name age` within a `.py` file results in the following.
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```
Executing the same command above in a `.js` file results in the following.
```javascript
class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
}
```

## Installation
For vim-plug
```vim
Plug 'superDross/class-builder'
```
