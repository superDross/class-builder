" class-builder.vim - ClassBuilder
" Author:       David Ross <https://github.com/superDross/>
" Version:      0.1

function! ClassBuilder(...)
  " create parameter substring
  if a:000[1:] !=# []
    let params = printf(', %s', join(a:000[1:], ', '))
  else
    let params = ''
  endif
  " append class text below cursor
  let class = [ 
        \ 'class ' . a:1 . ':',
        \ '    def __init__(self' . params . '):',
        \]
  let class += map(a:000[1:], "'        self.' . v:val . ' = ' . v:val")
  call append(line('.'), class)
  " place cursor at end of the last class line
  call cursor(line('.') + len(class), len(class[-1]))
endfunction

command! -nargs=+ Class :call ClassBuilder(<f-args>)
