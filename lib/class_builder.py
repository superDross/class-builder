import vim


class ClassBuilder:
    def __init__(self, class_name, *params):
        self.class_name = class_name
        self.params = params
        self.ext = self._get_file_extension()
        self.tab = self._get_shiftwidth()

    def _get_file_extension(self):
        return vim.eval("expand('%:e')")

    def _get_shiftwidth(self):
        if self.ext == 'py':
            return ' ' * 4
        return ' ' * int(vim.eval('&shiftwidth'))

    def _param_str(self):
        param_str = ', '.join(self.params)
        if self.ext and self.ext == 'py':
            param_str = f', {param_str}'
        return param_str

    def _ruby_class(self):
        class_list = [
            f'class {self.class_name}',
            f'{self.tab}def initialize({self._param_str()})'
        ]
        param_list = [f'{self.tab * 2}@{x} = x' for x in self.params]
        end = [f'{self.tab}end', 'end']
        return class_list + param_list + end

    def _php_class(self):
        class_list = [
            f'class {self.class_name} {{',
        ]
        param_list = [f'{self.tab}public ${x} = {x};' for x in self.params]
        end = ['}']
        return class_list + param_list + end

    def _python_class(self):
        class_list = [
            f'class {self.class_name}:',
            f'{self.tab}def __init__(self{self._param_str()}):',
        ]
        param_list = [f'{self.tab * 2}self.{x} = {x}' for x in self.params]
        return class_list + param_list

    def _javascript_class(self):
        class_list = [
            f'class {self.class_name} {{',
            f'{self.tab}constructor({self._param_str()}) {{'
        ]
        param_list = [f'{self.tab * 2}this.{x} = {x};' for x in self.params]
        end = [f'{self.tab}}}', '}']
        return class_list + param_list + end

    def build(self):
        method_dict = {
            'py': self._python_class,
            'js': self._javascript_class,
            'rb': self._ruby_class,
            'php': self._php_class
        }
        if self.ext not in method_dict.keys():
            raise TypeError(f'{self.ext} files are not supported')
        class_builder = method_dict[self.ext]
        class_list = class_builder()
        b = vim.current.buffer
        line = int(vim.eval("line('.')"))
        b.append(class_list, line)
