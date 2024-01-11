# event-templater
Criador de sites para eventos associados ao CCM-USP usando um templater.

O utilitário principal é o pagemanager.py, que gerencia o conteúdo das páginas existentes e roda a templating engine. Ele espera que as páginas criadas todas estejam na pasta content.

Simplesmente modifique as templates e o main.css com o que você quiser e rode pagemanager.py para criar ou updatar as páginas.

Um exemplo de página criada usando esse repositório está presente em http://wiki.cecm.usp.br/~moleculentos

Requer o jinja2 instalado via pip.

Comandos:
python pagemanager.py parse: Transforma informações do arquivo answers.csv emitido pelo nosso forms (https://forms.gle/K94s9TXeHJcce2x46) no nosso formato json.

python pagemanager.py create page: Cria uma página chamada page.

python pagemanager.py remove page: Apaga a página page.

python pagemanager.py update page: Updata a página page (soft update, não modifica o conteúdo).

python pagemanager.py update-all: Updata todas as páginas.

python pagemanager.py regenerate page: Regenera a página page usando a informação no json.

python pagemanager.py regenerate-all: Regenera todas as páginas interativamente (i.e. você precisa confirmar cada regeneração)

TODOs do repo:

Suporte automatizado para Open Graph

TODOs do site:

Favicon

Domínio oficial

RSS
