from bs4 import BeautifulSoup, Comment
from tqdm.auto import tqdm
from requests_html import HTMLSession
from colorama import Fore, Style

session = HTMLSession()

# variáveis do projeto
# projeto = ''

print(Fore.YELLOW)
projeto = str(input('Por favor, especifique o nome do projeto:\n'))
print(Style.RESET_ALL)

htdocs = f'C://xampp/htdocs/{projeto}/' # alterar para htdocs proprio

# inserir os arquivos para serem editados (sem .php)
f = []
g = 0

def get_mpis(URL):
    rm = session.get(URL + 'mapa-site')
    subMenuInfo = rm.html.find('.sitemap ul.sub-menu-info li a')

    for linkMPI in subMenuInfo:
        f.append(linkMPI.attrs['href'].split('/')[-1])

Error = { 'Não foi possível ler o(s) arquivo(s)':[],'Não foi possível criar o arquivo':[],'Não foi possível realizar o ajustes no(s) arquivo(s)':[],'Não foi possível recuperar o título da página':[], 'Não foi possível inserir após o H2': [], 'Falha na execução.': [], }

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
		Error['Não foi possível ler o(s) arquivo(s)'].append(f'=> {f}.php')

# montar url do temporario
def urlReplace(x, y):
	x = x.split('//')
	r = x[1].split('/')
	if not y:
		return 'http://mpitemporario.com.br/projetos/' + r[2] + '/'
	else:
		return 'http://mpitemporario.com.br/projetos/' + r[2] + '/' + y
	
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

			body = body.replace('<!-- include(\'inc/btn-modal.php\'); -->', "<? include('inc/btn-modal.php'); ?>")
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
			new_tag.append('<!-- include(\'inc/btn-modal.php\'); -->')

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
print('Iniciando Plano De Ação... Aguarde\n', Style.RESET_ALL)

if projeto:
	try:
		get_mpis(urlReplace(htdocs, False))
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

					if body != False:
						create(body, a)
						# print(body)
						g += 1
					else:
						Error['Falha na execução.'].append(f'=> {a}.php')

				except:
					Error['Não foi possível realizar o ajustes no(s) arquivo(s)'].append(f'=> {a}.php')

				del elements[:]
			
	except:
		print(Fore.RED)
		print('Não foi possível iniciar a função.', Style.RESET_ALL)

# # Coloca script no footer
# with open(htdocs + 'inc/footer.php', 'a', encoding='utf-8') as File:
# 	File.seek(-1)
# 	File.write("\n<script>$('body').on('mouseleave', function(){if($('.popup').length == 0){$('body').append(`<div class='popup'><p>Já vai?</p><p>Considere entrar em contato conosco, vamos ficar felizes em te ajudar</p><a href='<?=$url?>contato'>Contato</a><a href='javascript:;' class='close-popup'>Fechar</a></div>`);$('.popup').hide();$('.popup').fadeIn();$('.popup a.close-popup').on('click', function(){$('.popup').fadeOut();})}});</script>")
# # insere no style
# with open(htdocs + 'css/style.css', 'a', encoding='utf-8') as File:
# 	File.seek(-1)
# 	File.write('\n.popup{position:fixed;z-index:999;top:50px;left:0;right:0;margin:10px auto;width:400px;max-width:90%;background:#fff;border-radius:3px;box-shadow:0 2px 2px rgba(0,0,0,.5);display:flex;flex-wrap:wrap;justify-content:center;padding:20px;border:1px solid #f5f5f5}.popup p{font-size:24px;text-align:center;width:100%;margin:10px 0}.popup a{width:calc(50% - 20px);background:#f80000;margin:10px;text-align:center;padding:10px;color:#fff}#form-especialista{position:relative;float:left;width:100%;height:100%;box-sizing:border-box;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;padding:20px}#form-cta-form-rotulos-para-bebidas{background:#e2e2e2}.p-form{box-sizing:border-box;padding:0 40px;padding-top:20px}.p-form h2{font-size:32px;line-height:32px;color:#333233;display:block;font-weight:700;text-align:center;margin-bottom:10px;padding:0}.p-form h3{color:#b7b7b7;font-size:22px;line-height:28px;font-weight:400}.p-form h2,.p-form h3{text-align:center}#form-especialista .p-form{box-sizing:border-box;padding:20px}#form-especialista label{float:left;width:100%;color:#969696;font-size:16px;margin:0}#form-especialista input,#form-especialista select,#form-especialista textarea{outline:0;width:100%;box-sizing:border-box;padding:8px 5px;background:#fff;font-size:16px;font-weight:400;border:none;border:1px solid #c8c8c8;margin:10px 0;font-weight:700;border-radius:3px}#form-especialista .radio{float:left;clear:both;width:100%;margin:0}#form-especialista .radio input{display:inline-block;background-color:#fff;vertical-align:middle;font-size:18px;line-height:20px;width:auto!important;height:35px;margin:0;margin-right:5px;padding:5px}#form-especialista input[name=autorizo_contato_por_telefone]{width:auto!important;margin-right:5px}#form-especialista .notice{color:#969696}#form-especialista #cf_submit-cta-form-rotulos-para-bebidas{cursor:pointer;height:auto;text-align:center;text-decoration:none;font-weight:700;font-size:20px;word-break:break-all;line-height:1.2em;white-space:normal;vertical-align:middle;margin:15px auto 24px auto;padding:15px 20px 17px 20px;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;background:#f80000;border:1px solid #d60505;color:#fff}#form-especialista #cf_submit-cta-form-rotulos-para-bebidas:hover{filter:brightness(.9)}')

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