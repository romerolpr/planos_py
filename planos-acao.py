from bs4 import BeautifulSoup, Comment
from tqdm.auto import tqdm
from requests_html import HTMLSession
from colorama import Fore, Style

session = HTMLSession()

# variáveis do projeto
# projeto = ''

projeto = str(input('Por favor, especifique o nome do projeto:\n'))

htdocs = f'C://xampp/htdocs/{projeto}/' # alterar para htdocs proprio

# inserir os arquivos para serem editados (sem .php)
f = []

def get_mpis(URL):


    rm = session.get(URL + 'mapa-site')

    subMenuInfo = rm.html.find('.sitemap ul.sub-menu-info li a')

    for linkMPI in subMenuInfo:
        f.append(linkMPI.attrs['href'].split('/')[-1])

Error = { 'Não foi possível ler o(s) arquivo(s)':[],'Não foi possível criar o arquivo':[],'Não foi possível realizar o ajustes no(s) arquivo(s)':[],'Não foi possível recuperar o título da página':[], 'Não foi possível inserir após o H2': [] }

# le arquivo e recupera valores
def file_read(f):
	content = []
	import os.path
	try:
		with open(f + '.php', 'r', encoding='utf8') as file:
			lines = file.readlines()
			for elem in lines:
				content.append(elem)
				# string converter
			return ''.join(map(str, content))
	except IOError:
		return False	
		Error['Não foi possível ler o(s) arquivo(s)'].append(f'=> {f}.php')

# montar url do temporario
def urlReplace(x, y):
	x = x.split('//')
	r = x[1].split('/')
	return 'http://mpitemporario.com.br/projetos/' + r[2] + '/' + y

def urlReplaceMPI(x):
	x = x.split('//')
	r = x[1].split('/')
	return 'http://mpitemporario.com.br/projetos/' + r[2] + '/'

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
		with open(f'./projetos/{arquivo}' + '.php', 'w', encoding='utf8') as f:

			#cria
			f.write(body)
			f.write('</html>')
	except: 
	    Error['Não foi possível criar o arquivo'].append(f'=> {file}.php')

# faz o ajuste nos strongs do projeto
def add_content(t, html, a):

	# armazenando elementos
	content = []
	try:

		# criando o soup em html
		soup = BeautifulSoup(mask(html, True), "html.parser")
		title = t.strip()

		# tenta rodar os ajustes

		for article in soup.select('article'):

			new_tag = soup.new_tag("div")
			new_tag.append("<!-- include('inc/btn-modal.php'); -->")

			h2 = article.find('h2')

			# verifica se o paragrafo tem strong
			if h2:
				h2.insert_after(new_tag)
			else:
				Error['Não foi possível inserir após o H2'].append(f'\n=> {a}')	


		# retorna novo código
		for elem in soup.prettify(formatter=None):
			content.append(elem)
		value = ''.join(map(str, content))

		return mask(value, False)

	except:
		return False


# Inicia função principal para executar as correções
print(Fore.YELLOW)
print('Iniciando correções... Aguarde\n', Style.RESET_ALL)

if projeto:
	try:
		get_mpis(urlReplaceMPI(htdocs))
		# print(f)

		for a in tqdm(f):

			r = session.get(urlReplace(htdocs, a))
			# constroi o arquivo
			html = file_read(htdocs + a.strip())
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
					
					create(body, a)

				except:
					Error['Não foi possível realizar o ajustes no(s) arquivo(s)'].append(f'=> {a}.php')

				del elements[:]
			
	except:
		print(Fore.RED)
		print('Não foi possível iniciar a função.', Style.RESET_ALL)

# Coloca script no footer
with open(htdocs + 'inc/footer.php', 'a', encoding='utf8') as File:
	File.write("<script>$('body').on('mouseleave', function(){if($('.popup').length == 0){$('body').append(`<div class='popup'><p>Já vai?</p><p>Considere entrar em contato conosco, vamos ficar felizes em te ajudar</p><a href='<?=$url?>contato'>Contato</a><a href='javascript:;' class='close-popup'>Fechar</a></div>`);$('.popup').hide();$('.popup').fadeIn();$('.popup a.close-popup').on('click', function(){$('.popup').fadeOut();})}});</script>")

print(Fore.RED)
# Exibe log na tela
for errosItens in Error.keys():

    if len(Error[errosItens]) > 0:
        print(errosItens+'\n')
        for errosValores in Error[errosItens]:
            print(errosValores)
        print('\n')
    else:
    	print(Fore.GREEN)
    	print('Ajustes realizados com sucesso!')	
    	break

print(Style.RESET_ALL)

input('\nFinalizado. Aperte "ENTER" para encerrar o programa.')