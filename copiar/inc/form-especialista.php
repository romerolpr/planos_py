<?php

$post = filter_input_array(INPUT_POST, FILTER_DEFAULT);
if (isset($post) && isset($post['EnviaContato2'])):

//Inclue o verificador de Spammers do formulário
include('inc/searchSpammer.inc.php');

//Armazena o reCapcha
$recapt = $post['g-recaptcha-response'];

//Remove o submit e o reCpatcha para validação de campos vazios
unset($post['EnviaContato2'], $post['g-recaptcha-response']);
//Arquivos válidos que podem ser enviados
$MimeTypes = array(
'application/pdf',
'application/msword',
'application/vnd.ms-excel',
'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
'application/x-excel',
'application/x-msexcel',
'image/png',
'image/pjpeg',
'image/jpeg',
'image/jpg',
'image/pjpeg',
'image/gif'
);
//Verifica se os campos obrigatórios foram todos preenchidos

if (in_array('', $post)):
echo '<script>'
. '$(function () {';
echo 'swal("Aviso!", "Campos com * são obrigatórios.", "info");';
echo '});'
. '</script>';
//Verifica se existem spammers nos campos do formulário
elseif (SearchSpammer($post)):

//Inclui o emailFake, que fará a notificação aos adms do site
include('especialista-envia.php');
//Verifica se existe anexo para envio e se o anexo está na lista do MimeTypes
elseif (isset($_FILES['anexo']) && !empty($_FILES['anexo']['tmp_name']) && !in_array($_FILES['anexo']['type'], $MimeTypes)):
echo '<script>'
. '$(function () {';
echo 'swal("Aviso!", "Escolha um arquivo válido para enviar como anexo da mensagem", "info");';
echo '});'
. '</script>';
else:
//Caso as condições sejam atendidas, o reCaptcha volta para o post e o anexo é adicionado ao post
$post['g-recaptcha-response'] = $recapt;
$post['anexo'] = ($_FILES['anexo']['tmp_name'] ? $_FILES['anexo'] : null);
//Arquivo que faz a verificação do reCaptcha e o envio dos e-mails
include('especialista-envia.php');
endif;
endif;

?>

<a id="especialista-modal" href="javascript:;" data-src="#banner" class="lightbox-form btn btn-orc" title="Quero Falar com um Especialista" rel="nofollow">Quero
Falar com um Especialista</a>
	
		
		<div style="display: none;width: 50%;" id="banner">
			
			<div id="orcamento">
				<div role="main" id="cta-form-rotulos-para-bebidas">
				<section id="form-cta-form-rotulos-para-bebidas">
					<h2 style="display: none;"><?=$h1?></h2>
			  <div id="form-container-cta-form-rotulos-para-bebidas" class="cleanslate">
			    <div id="conversion-cta-form-rotulos-para-bebidas" class="wrapper">
					<div class="p-form">
				        <h2>Fale com um Especialista</h2>
				        <!-- <h3>Fale com um Especialista!</h3> -->
					</div>
			      <section>
			      	<h2 style="display: none;"><?=$h1?></h2>
			  <form id="form-especialista" enctype="multipart/form-data" method="POST">


			    <div id="error-container-cta-form-rotulos-para-bebidas" class="hide">
			      <p>Preencha corretamente os campos marcados</p>
			    </div>

			    <div class="field">
			<label for="name">Nome*</label><input type="text" name="name" id="name" value="" class="form-control required js-text" required="required">
			</div>
			<div class="field">
			<label for="email">Email*</label><input type="email" name="email" id="email" value="" class="form-control required js-email" required="required" data-input-id="00c999">
			</div>
			<div class="field">
			<label for="empresa">Empresa*</label><input type="text" name="empresa" id="empresa" value="" class="form-control required js-text" required="required">
			</div>
			<div class="field">
			<label for="telefone">Telefone*</label><input type="tel" name="telefone" id="telefone" value="" class="form-control phone required js-tel" required="required">
			</div>
			<div class="field">

				<label for="opcao_que_melhor_define_voce_meio_de_funil">Marque a opção que melhor define você*</label>

				<select name="opcao_que_melhor_define_voce_meio_de_funil" id="opcao_que_melhor_define_voce_meio_de_funil" class="form-control required js-field-opcao_que_melhor_define_voce_meio_de_funil" required="required">
					<option value="">Selecione</option>
					<!-- <option value="Agência - Sou dono ou trabalho em uma Agência">Agência - Sou dono ou trabalho em uma Agência</option> -->
					<option value="Revenda">Revenda</option>
					<option value="Consultor">Consultor</option>
					<option value="Sócio(a)/Gerente">Sócio(a)/Gerente</option>
					<option value="Compras">Compras</option>
					<option value="Logística">Logística</option>
					<option value="Marketing">Marketing</option>
	<!-- 				<option value="P&amp;D - Trabalho com Desenvolvimento de Produtos em uma indústria ou comércio">P&amp;D - Trabalho com Desenvolvimento de Produtos em uma indústria ou comércio</option> -->
					<option value="Qualidade">Qualidade</option>
					<option value="Outros">Outros</option>
				</select>

			</div>

			<div class="field">

				<label for="detalhes_do_produto_que_possui_interesse">Detalhes do produto (outras informações)*</label>
				<textarea name="detalhes_do_produto_que_possui_interesse" id="detalhes_do_produto_que_possui_interesse" class="form-control required js-field-detalhes_do_produto_que_possui_interesse" required="required"></textarea>

			</div>

			<div class="field">
				<label for="quantidade_total_que_tem_interesse_em_adquirir_original">Quantidade (total) que tem interesse em adquirir*</label>
				<input type="number" name="quantidade_total_que_tem_interesse_em_adquirir_original" id="quantidade_total_que_tem_interesse_em_adquirir_original" value="" placeholder="" required="required">	
			</div>

			<div class="field">
				<label for="investimento_empresa">Qual investimento sua empresa deseja fazer?*</label>
				<input type="number" name="investimento_empresa" id="investimento_empresa" value="" required="required">
			</div>

			<div class="field">
			<label for="entrega">Para quando você precisa do produto entregue?*</label><select name="entrega" id="entrega" class="form-control required js-field-entrega" required="required"><option value="">Selecione</option>
			<option value="Em menos de 1 semana">Em menos de 1 semana</option>
			<option value="Até 15 dias">Até 15 dias</option>
			<option value="Até 30 dias">Até 30 dias</option>
			<option value="Até 90 dias">Até 90 dias</option>
			<option value="Mais de 90 dias">Mais de 90 dias</option></select>
			</div>
			<div class="field">
			<label for="frequencia">Com qual frequência deseja comprar?*</label><select name="frequencia" id="frequencia" class="form-control required js-field-frequencia" required="required"><option value="">Selecione</option>
			<option value="Compra única">Compra única</option>
			<option value="Todo mês">Todo mês</option>
			<option value="A cada 3 meses">A cada 3 meses</option>
			<option value="A cada 6 meses">A cada 6 meses</option>
			<option value="Uma vez por ano">Uma vez por ano</option></select>
			</div>
			<div class="field"><label class="text-line-break" for="autorizo_contato_por_telefone"><input type="checkbox" name="autorizo_contato_por_telefone" id="autorizo_contato_por_telefone" value="1" required="required">Autorizo contato por Telefone</label></div>

			    <div class="actions">
			      <input type="submit" class="call_button" id="cf_submit-cta-form-rotulos-para-bebidas" value="Quero Falar com um Especialista">
			      <img src="//d335luupugsy2.cloudfront.net/images/ajax-loader.gif" id="ajax-loader-cta-form-rotulos-para-bebidas" class="hide" alt="#{Enviando...}">
			    </div>

			      <p class="notice">Entraremos em contato muito em breve! Seus dados não serão utilizados para nenhum outro fim. </p>

			    <div style="position: fixed!important; left: -5000px!important;">
			      <input type="text" name="autoriza_contato" tabindex="-1" value="Autorizo">
			      <input type="text" name="EnviaContato2" tabindex="-1" value="should_not_change">
			    </div>
			  </form>
			</section>
			    </div>
			  </div>
			</section>
		</div> 

		</div>

	</div>

<script>
$(document).ready(function() {$(".lightbox-form").fancybox();});
</script>