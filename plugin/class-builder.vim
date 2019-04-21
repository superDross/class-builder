" class-builder.vim - Class Builder
" Author:       David Ross <https://github.com/superDross/>
" Version:      0.2

python3 << EOF
import os
import sys
import vim

# Get the Vim variable to Python
plugin_path = vim.eval("expand('<sfile>:p:h')")
# Get the absolute path to the lib directory
python_module_path = os.path.abspath('%s/../lib' % (plugin_path))
# Append it to the system paths
sys.path.append(python_module_path)

from class_builder import class_factory
EOF

command! -nargs=+ Class :python3 class_factory(<f-args>)
