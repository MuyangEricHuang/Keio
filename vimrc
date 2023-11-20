" Last update: 02/26/2020

set expandtab "タブ入力を複数の空白入力に置き換える
set tabstop=4 "画面上でタブ文字が占める幅
set shiftwidth=4 "自動インデントでずれる幅
set softtabstop=4 "連続した空白に対してタブキーやバックスペースキーでカーソルが動く幅
set autoindent "改行時に前の行のインデントを継続する
set smartindent "改行時に入力された行の末尾に合わせて次の行のインデントを増減する
set ignorecase "検索時に大文字小文字を無視 (noignorecase:無視しない)
set smartcase "大文字小文字の両方が含まれている場合は大文字小文字を区別
set incsearch "インクリメンタルサーチ
set hlsearch "検索ハイライト
set noswapfile
set number
set wrap "長い行を折り返して表示
set showmode
set title
set showmatch "閉じ括弧入力時に対応する括弧の強調
set backspace=indent,eol,start

set statusline=%F "ファイル名表示
set statusline+=%m "変更チェック表示
set statusline+=%= "これ以降は右寄せ表示
set statusline+=%r "読み込み専用かどうか表示
set statusline+=\ <%l/%L> " 現在行数/全行数
set statusline+=\ %y "ファイルタイプ表示
set statusline+=\ %{has('multi_byte')&&\&fileencoding!=''?&fileencoding:&encoding} "file encoding
set statusline+=[%{&fileformat}] "ファイルフォーマット表示
set statusline+=\ @%{matchstr(hostname(),'\\w\\+')} "ホスト名表示
set laststatus=2 "ステータスラインを常に表示(0:表示しない、1:2つ以上ウィンドウがある時だけ表示)
 
nnoremap <Down> gj
nnoremap <Up>   gk
imap jj <esc>

syntax on

" Created by M.H.
