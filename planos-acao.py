# v1.0 (Beta)

import os
from bs4 import BeautifulSoup, Comment
from tqdm.auto import tqdm
from requests_html import HTMLSession
from colorama import Fore, Style, init
import sys

# Variáveis Pessoais (alterar)
htdocs 	= 'E://xampp/htdocs/Git/'	
code 	= 'include(\'inc/btn-modal.php\');' # Código a ser inserido nos aquivos
web 	= 'mpitemporario.com.br/projetos/' # site para montar a sessao

# Sistema editável
vAll 	= True # Quando True resgata todas as MPI'S automaticamente
f 		= []

# lista de variáveis para exibir no comando
VAR = {'htdocs': htdocs, 'code': code, 'url': web}
init(autoreset=True)

# comandos do sistema
def commands(console):

	# help
	if ' help' in console or 'help' == console:
		print('planos_py, versão 1.0 (beta)')
		print('Comandos de execução')
		print(' -a     ───────  Inicia o programa.')
		print(' -edit  ───────  Edita uma variável existente do sitema. [var] [...] -edit')
		print(' -p     ───────  Imprime na tela uma variável existente. [var] -p')
		print('Comandos rápidos')
		print(' clear  ───────  Limpa todos os elementos na tela.')
		print(' exit   ───────  Encerra todos os processos.')
		print(' help   ───────  Exibe comandos completos do sistema.')
		print(' var    ───────  Exibe todas as variáveis do sistema.')

	if ' clear' in console or 'clear' == console:
		clear = lambda: os.system('cls')
		clear()
	if 'exit' == console:
		sys.exit()
	if 'var' == console:
		print('Variáveis do sistema')
		for item in VAR.keys():
			print(' ' + item + ': ' + VAR[item])
	if ' -p' in console:
		for event in VAR:
			if console.split(' -p')[0] in event:
				print(VAR[event])

	if ' -edit' in console:
		for event in VAR:
			if console.split(' ')[0].strip() in event:
				VAR[event] = console.split(' ')[1]
				print(VAR[event])

while True:

	# Sistema
	Start 		= False
	terminal 	= ''

	# projeto
	while ' -a' not in terminal:
		print(Fore.YELLOW + '\nEspecifique o nome do projeto' + Fore.CYAN + ' (-a para iniciar)')
		terminal = str(input('$ '))
		# definindo funções do console
		if terminal not in ' -a':
			commands(terminal)
		else:
			Start = True if terminal else False

	# Variáveis interativas
	projeto 	= terminal.split(' -a')[0].strip()
	workplace 	= VAR['htdocs'] + projeto + '/'
	g 			= []

	# Programa

	# Rewrite url
	def url_replace(url, file):
		rewrite = 'http://' + web + projeto + '/' if not file else 'http://' + web + projeto + '/' + file
		return rewrite

	def get_mpis(URL):
		rm = session.get(URL + 'mapa-site')
		subMenu = rm.html.find('.sitemap ul.sub-menu-info')
		subMenuInfo = rm.html.find('.sitemap ul.sub-menu-info li a') if subMenu else rm.html.find('.sitemap ul.sub-menu li a')
		for linkMPI in subMenuInfo:
			f.append(linkMPI.attrs['href'].split('/')[-1])

	Error = { 'Não foi possível ler o(s) arquivo(s)':[],'Não foi possível criar o arquivo':[],'Não foi possível realizar o ajustes no(s) arquivo(s)':[],'Não foi possível recuperar o título da página':[], 'Não foi possível inserir após o H2': [], 'Falha na execução.': [], 'Não foi possível montar a sessão do projeto': [], }
	Log = { 'Não foi possível inserir "{}" no arquivo'.format(VAR['code']): [],}

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

				body = body.replace('<!-- {} -->'.format(VAR['code']), '<? {} ?>'.format(VAR['code']))
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
				new_tag.append('<!-- {} -->'.format(VAR['code']))

				h2 = article.find('h2')

				# verifica se o article tem h2
				if h2:
					h2.insert_after(new_tag)
				else:
					Log['Não foi possível inserir "{}" no arquivo'.format(VAR['code'])].append(f'\n=> {a}')	


			# retorna novo código
			for elem in soup.prettify(formatter=None):
				content.append(elem)
			value = ''.join(map(str, content))

			return mask(value, False)

		except:
			return False

	# Inicia função principal para executar as correções
	# informa o projeto e metodo
	print(Fore.MAGENTA + f'\nmethod -a ' + Fore.YELLOW + '{}'.format('/' + workplace.split('//')[-1]) + Fore.CYAN + ' (Processando...)\n')

	session = HTMLSession()

	try:
		
		try:

			if vAll:
				get_mpis(url_replace(workplace, False))

		except:

			Error['Não foi possível recuperar as palavras chaves do projeto'].append(f'=> {url_replace(workplace, a)}')

		else:

			for a in tqdm(f):

				# monta sessão
				r = session.get(url_replace(workplace, a))

				# lê e monta o arquivo
				html = file_read(workplace + a.strip())
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
					Error['Não foi possível recuperar o título da página'].append(f'=> {url_replace(workplace, a)}')
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
		print(Fore.RED + 'Não foi possível iniciar a função.')

	# Exibe log na tela
	for errosItens in Error.keys():
	    if len(Error[errosItens]) > 0:

	        print(Fore.RED + errosItens)

	        for errosValores in Error[errosItens]:
	            print(Fore.RED + errosValores)

	        msg = 'Falha ao tentar executar 1 ou mais funções.'
	    else:
	    	msg = 'Foram realizados ({}) planos de ação no projeto\n=> {}'.format(len(g), url_replace(workplace, False))

	for logItens in Log.keys():
		if len(Log[logItens]) > 0:
		    print('!!! AVISO !!!\n')
		    print(Fore.YELLOW + logItens)
		    for logValores in Log[logItens]:
		        print(Fore.YELLOW + logValores)

	print('\n')
	if len(g) > 0:
		print(Fore.GREEN + msg)
	else:
		print(Fore.RED + msg)	

	Start = False
	workplace = VAR['htdocs']

	del f[:]