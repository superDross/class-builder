import vim


class ClassBuilder:
    def __init__(self, class_name, params):
        self.class_name = class_name
        self.params = params
        self.ext = self.get_file_extension()
        self.tab = self._get_shiftwidth()

    @staticmethod
    def get_file_extension():
        return vim.eval("expand('%:e')")

    def _get_shiftwidth(self):
        if self.ext == 'py':
            return ' ' * 4
        return ' ' * int(vim.eval('&shiftwidth'))

    def param_str(self):
        param_str = ', '.join(self.params)
        if self.params and self.ext == 'py':
            param_str = f', {param_str}'
        return param_str

    def _build_class_list(self):
        pass

    def build(self):
        class_list = self._build_class_list()
        b = vim.current.buffer
        line = int(vim.eval("line('.')"))
        b.append(class_list, line)


class PythonClass(ClassBuilder):
    def __init__(self, class_name, params):
        super().__init__(class_name, params)

    def _build_class_list(self):
        class_list = [
            f'class {self.class_name}:',
            f'{self.tab}def __init__(self{self.param_str()}):',
        ]
        param_list = [f'{self.tab * 2}self.{x} = {x}' for x in self.params]
        return class_list + param_list


class RubyClass(ClassBuilder):
    def __init__(self, class_name, params):
        super().__init__(class_name, params)

    def _build_class_list(self):
        class_list = [
            f'class {self.class_name}',
            f'{self.tab}def initialize({self.param_str()})'
        ]
        param_list = [f'{self.tab * 2}@{x} = x' for x in self.params]
        end = [f'{self.tab}end', 'end']
        return class_list + param_list + end


class PHPClass(ClassBuilder):
    def __init__(self, class_name, params):
        super().__init__(class_name, params)

    def _build_class_list(self):
        class_list = [
            f'class {self.class_name} {{',
        ]
        param_list = [f'{self.tab}public ${x} = {x};' for x in self.params]
        end = ['}']
        return class_list + param_list + end


class JavaScriptClass(ClassBuilder):
    def __init__(self, class_name, params):
        super().__init__(class_name, params)

    def _build_class_list(self):
        class_list = [
            f'class {self.class_name} {{',
            f'{self.tab}constructor({self.param_str()}) {{'
        ]
        param_list = [f'{self.tab * 2}this.{x} = {x};' for x in self.params]
        end = [f'{self.tab}}}', '}']
        return class_list + param_list + end


def class_factory(class_name, *params):
    method_dict = {
        'py': PythonClass,
        'js': JavaScriptClass,
        'rb': RubyClass,
        'php': PHPClass
    }
    ext = ClassBuilder.get_file_extension()
    if ext not in method_dict.keys():
        raise TypeError(f'{ext} files are not supported')
    class_builder = method_dict[ext](class_name, params)
    class_builder.build()
