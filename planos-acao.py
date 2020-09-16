# Leia README.md para utilizar a aplicação corretamente.

from bs4 import BeautifulSoup, Comment
from tqdm.auto import tqdm
from requests_html import HTMLSession
from colorama import Fore, Style

print(Fore.YELLOW)
projeto = str(input('Por favor, especifique o nome do projeto: '))
print(Style.RESET_ALL)

# alterar para htdocs proprio
htdocs = f'E://xampp/htdocs/Git/{projeto}/'

# código a ser inserido
code = 'include(\'btn-modal.php\');'

# "True" aplica o plano em todas as palavras chaves do projeto. 
# "False", utiliza a lista "f" para realizar os planos
vAll = True
f = []
g = []

def get_mpis(URL):
	rm = session.get(URL + 'mapa-site')
	subMenuInfo = rm.html.find('.sitemap ul.sub-menu-info li a')
	for linkMPI in subMenuInfo:
		f.append(linkMPI.attrs['href'].split('/')[-1])

Error = { 'Não foi possível ler o(s) arquivo(s)':[],'Não foi possível criar o arquivo':[],'Não foi possível realizar o ajustes no(s) arquivo(s)':[],'Não foi possível recuperar o título da página':[], 'Não foi possível inserir após o H2': [], 'Falha na execução.': [], 'Não foi possível montar a sessão do projeto': [], }
Log = { f'Não foi possível inserir "{code}" no arquivo': [],}

# le arquivo e recupera valores
def file_read(f):
	content = []
	import os.path
	try:
		with open(f + '.php', 'r', encoding='utf-8') as file:
			lines = file.readlines()
			for elem in lines:
				content.append(elem)
				# string converter
			return ''.join(map(str, content))
	except IOError:
		return False	

# montar url do temporario
def urlReplace(x, file):
	x = x.split('//')[1]
	project = x.split('/')[2] if 'git' not in htdocs.lower() else x.split('/')[3] 
	if not file:
		return 'http://www.' + project + '/'
	else:
		return 'http://www.' + project + '/' + file
	
# variáveis para mascara
elements = []
msk = '!!!PHP!!!'

# funções pra fazer a remoção
def remove(d):
    elements.append(d.group())
    return msk
def add(e):
    return elements.pop(0)

# funcao para aplicar/ retirar mascara no codigo
def mask(c, i):
	import re
	try:

		# aplica a mascara
		m = re.sub(r"<\?.*\?>", remove, c)
		soup = BeautifulSoup(m, "html.parser")
		if i == True:
			mask = re.sub(msk, remove, soup.prettify())
		else:
			mask = re.sub(msk, add, soup.prettify())
	except:
		mask = False

	return mask

# cria o arquivo
def create(body, file):
	from pathlib import Path
	arquivo = projeto + '/' + file
	# realiza a criacao dos arquivos
	try:

		# faz a criacao da pasta
		Path(f'./projetos/{projeto}').mkdir(parents=True, exist_ok=True)

	    # faz a criacao dos arquivos
		with open(f'./projetos/{arquivo}' + '.php', 'w', encoding='utf-8') as f:

			body = body.replace(f'<!-- {code} -->', f'<? {code} ?>')
			#cria
			f.write(body)
			f.write('</html>')
	except: 
	    Error['Não foi possível criar o arquivo'].append(f'=> {file}')

# insere o codigo
def add_content(t, html, a):

	# armazenando elementos
	content = []
	try:

		# criando o soup em html
		soup = BeautifulSoup(mask(html, True), "html.parser")

		# tenta rodar os ajustes

		for article in soup.select('article'):

			new_tag = soup.new_tag("div")
			new_tag.append(f'<!-- {code} -->')

			h2 = article.find('h2')

			# verifica se o article tem h2
			if h2:
				h2.insert_after(new_tag)
			else:
				Log[f'Não foi possível inserir "{code}" no arquivo'].append(f'\n=> {a}')	


		# retorna novo código
		for elem in soup.prettify(formatter=None):
			content.append(elem)
		value = ''.join(map(str, content))

		return mask(value, False)

	except:
		return False


# Inicia função principal para executar as correções
print(Fore.YELLOW)
print('Iniciando plano de ação... Aguarde\n', Style.RESET_ALL)

session = HTMLSession()

if projeto:
	try:
		
		try:

			if vAll:
				get_mpis(urlReplace(htdocs, False))

		except:

			Error['Não foi possível recuperar as palavras chaves do projeto'].append(f'=> {urlReplace(htdocs, a)}')

		else:

			for a in tqdm(f):

				# monta sessão
				r = session.get(urlReplace(htdocs, a))

				# lê e monta o arquivo
				html = file_read(htdocs + a.strip())
				if not html:
					# exibe erro se nao conseguir ler o arquivo
					Error['Não foi possível ler o(s) arquivo(s)'].append(f'=> {f}')
					break
				# retorna o title da pagina
				try:
					t = r.html.find('head title')
					for v in t:
						title = v.text.split('-')[0]
				except:
					Error['Não foi possível recuperar o título da página'].append(f'=> {urlReplace(htdocs, a)}')
				else:
					try:
						
						# Após receber todos os valores com sucesso, realiza os ajustes e retira a máscara do código
						body = add_content(title, html, a)

						if body != False:
							create(body, a)
							# print(body)
							g.append(a)
						else:
							Error['Falha na execução.'].append(f'=> {a}')

					except:
						Error['Não foi possível realizar o ajustes no(s) arquivo(s)'].append(f'=> {a}')

					del elements[:]
			
	except:
		print(Fore.RED)
		print('Não foi possível iniciar a função.', Style.RESET_ALL)

# Exibe log na tela
print(Fore.RED)
for errosItens in Error.keys():
    if len(Error[errosItens]) > 0:

        print(errosItens)

        for errosValores in Error[errosItens]:
            print(errosValores)

        msg = 'Falha ao tentar executar 1 ou mais funções.'
    else:
    	msg = 'Foram realizados ({}) planos de ação no projeto\n=> {}'.format(len(g), urlReplace(htdocs, False))

print(Fore.YELLOW)
for logItens in Log.keys():
	if len(Log[logItens]) > 0:
	    print('!!! AVISO !!!\n')
	    print(logItens)
	    for logValores in Log[logItens]:
	        print(logValores)

if len(g) > 0:
	print(Fore.GREEN)
else:
	print(Fore.RED)

print(msg, Style.RESET_ALL)	

input('\nFinalizado. Aperte "ENTER" para encerrar o programa.')