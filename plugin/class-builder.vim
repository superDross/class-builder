" class-builder.vim - Class Builder
" Author:       David Ross <https://github.com/superDross/>
" Version:      0.1

function! FormatParams(params)
  if a:params !=# []
    let params = join(a:params, ', ')
  else
    let params = ''
  endif
  return params
endfunction

function! PythonClassBuilder(classname, params)
  let param_string = FormatParams(a:params)
  if a:params !=# []
    let param_string = ', ' . param_string
  endif
  let class = [ 
        \ 'class ' . a:classname . ':',
        \ '    def __init__(self' . param_string . '):',
        \]
  let class += map(a:params, "'        self.' . v:val . ' = ' . v:val")
  call append(line('.'), class)
  return class
endfunction

function! JavaScriptClassBuilder(classname, params)
  let param_string = FormatParams(a:params)
  let class = [
        \ 'class ' . a:classname . ' {',
        \ '  constructor(' . param_string . ') {',
        \ ]
  let class += map(a:params, "'    this.' . v:val . ' = ' . v:val . ';'")
  let class += ['  }', '}']
  call append(line('.'), class)
  return class
endfunction

function! ClassBuilder(...)
  let ext = expand('%:e')
  let classname = a:1
  let params = a:000[1:]
  if ext ==# 'py'
    let class = PythonClassBuilder(classname, params)
  elseif ext ==# 'js'
    let class = JavaScriptClassBuilder(classname, params)
  else
    echoerr ext . ' files are not supported'
    return 1
  endif
  call cursor(line('.') + len(class), len(class[-1]))
endfunction


command! -nargs=+ Class :call ClassBuilder(<f-args>)
