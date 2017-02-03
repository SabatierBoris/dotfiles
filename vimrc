"Plugin installation
call plug#begin('~/.vim/plugged')
Plug 'scrooloose/nerdtree'
Plug 'metakirby5/codi.vim'
Plug 'w0rp/ale'
Plug 'ramele/agrep'
Plug 'LucHermitte/lh-vim-lib'
Plug 'LucHermitte/local_vimrc'

Plug 'fatih/vim-go'
Plug 'powerline/powerline'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
call plug#end()

"Nerdtree plugin conf
map <C-n> :NERDTreeToggle<CR>
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif

"agrep shortcut
let agrep_win_sp_mod = 'botright vert'
noremap <expr> <C-f> ((bufwinnr('Agrep')==-1)?':Agrep -R <cword><CR>':':Anext<CR>')
noremap <expr> <S-f> ((bufwinnr('Agrep')==-1)?'':':Aclose<CR>')

"Local_vimrc plugin conf
call lh#local_vimrc#munge('whitelist', $HOME.'/workspaces/')










"Airline plugin conf
let g:airline#extensions#tabline#enabled = 1
let g:airline_powerline_fonts=1
set laststatus=2
map <tab> :bn<CR>
map <s-tab> :bp<CR>






"General option
set nocompatible
set number
set autoread
set nowrap

































""============================================================================="
"" Fichier .vimrc de Boris SABATIER ==========================================="
"" Créé le 29/02/2012 =========================================================" 
""============================================================================="
"
""============================================================================="
"" Options général ============================================================"
""============================================================================="
"set nocompatible	" Utilisation de vim a font =============================="
"set mouse=a 		" Activation de la sourie ================================"
""============================================================================="
"
""============================================================================="
"" Options d'affichage ========================================================"
""============================================================================="
"colorscheme lucius	" Utilisation du thème lucius ============================"
"LuciusBlackLowContrast " Utilisation de LuciusBlackLowContrast ==============="
"syntax enable		" Active la coloration syntaxique ========================"
"set number			" Active la numerotation des ligne ======================="
"set autoread		" Mise à jour si modification exterieur =================="
""============================================================================="
"
""============================================================================="
"" Options d'éditions ========================================================="
""============================================================================="
"set autoindent		" Activation de l'indentation ============================"
"set smartindent		" Indentation plus intelligente =========================="
"set history=50		" Historique de 50 commandes ============================="
"set ruler			" Affiche la possition dans le fichier ==================="
"set showcmd			" Affichage la commande en cours ========================="
"set tabstop=4		" Un tab affiche 4 caractères ============================"
"set shiftwidth=4	" Un décalage prend 4 caractères (1 tab) ================="
"set noexpandtab		" Ne pas remplacé les tab par des espaces ================"
"set showmatch		" Vérification de la présence des {([ et ])} ============="
"set tw=0			" Une ligne n'a pas de taille max ========================"
"set nowrap			" Pas de retour a la ligne si ça dépace l'écran =========="
""============================================================================="
"
""============================================================================="
"" Options de recherche ======================================================="
""============================================================================="
"set incsearch	" recherche incrémental ======================================"
"set hlsearch	" Surligne les résultats ====================================="
"set ignorecase	" Ignore la case ============================================="
""============================================================================="
"
""============================================================================="
"" Options de folding ========================================================="
""============================================================================="
"set foldcolumn=0		" Une colone pour le repert des fold ================="
"set foldmethod=syntax	" Fold detecté grace a la syntax ====================="
""============================================================================="
"
""============================================================================="
"" Options des fichiers ======================================================="
""============================================================================="
"filetype plugin on	" Chargement des plugin =================================="
"filetype indent on	" Detection des fichiers pour l'indentation =============="
""============================================================================="
"
""============================================================================="
"" Personnalisation des maps =================================================="
""============================================================================="
"" tab pour passer a l'onglet suivant ========================================="
"map <tab> gt
"" swift-tab pour passer a l'onglet préceedent ================================"
"map <s-tab> gT
""============================================================================="
