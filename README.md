# event-templater
Criador de sites para eventos associados ao CCM-USP usando um templater.

O utilitário principal é o pagemanager.py, que gerencia as páginas existentes para criar a barra de navegação e roda a templating engine.

Simplesmente modifique template.html com o que você quiser e rode pagemanager.py para criar ou updatar as páginas.

Você também pode modificar o main.css presente na pasta content, para modificar o estilo da página sem mexer no HTML.

Um exemplo de página criada usando esse repositório está presente em http://wiki.cecm.usp.br/~sunny/demo/home.html

Requer o jinja2 instalado via pip.

Comandos:

python pagemanager.py create page: Cria uma página chamada page.

python pagemanager.py delete page: Apaga a página page.

python pagemanager.py update page: Updata a página page.

python pagemanager.py update-all: Updata todas as páginas.
