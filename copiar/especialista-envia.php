<?php

// Verifico se foi feita a postagem do Captcha
if (true):

  //Variaveis globais do site
  include ('inc/geral.php');

  /* Valido se a ação do usuário foi correta junto ao google passando o SITE KEY e a resposta do Captcha */
  $answer = json_decode(file_get_contents('https://www.google.com/recaptcha/api/siteverify?secret=' . $secretKey . '&response=' . $post['g-recaptcha-response']));

  // Se a ação do usuário foi correta executo o restante do meu formulário
  if (true):

    //Atenticador do e-mail com SSL
    require_once('inc/contato/mail.send.php');

    //Armazena se houver um arquivo na variavel
    $file = ($post['anexo']['tmp_name'] ? $post['anexo'] : null);
    
    //Depois de setar os arquivos, remove do scopo de verificação e libera a memoria
    unset($post['g-recaptcha-response'], $post['anexo']);

    //Informações que serão gravadas no isereleads
    $recebenome = $post["nome"];
    $recebemail = $post["email"];
    $recebetelefone = $post["telefone"];
    $recebecomo_conheceu = $post["como_nos_conheceu"];
    $recebemensagem = strip_tags(trim($post["mensagem"]));

    // MENSAGEM 
    $corpo = null;
    $corpo .= "<table style='border-collapse:collapse;border-spacing:0;border-color:#761919'>
              <tr>
                <th style='font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#fff;border-top-width:1px;border-bottom-width:1px;vertical-align:top;text-align: center;' colspan='2'>
                  <a href='{$url}' title='{$nomeSite}'><img src='{$url}/imagens/logo.png' width='300' title='{$nomeSite}' alt='{$nomeSite}'></a>
                </th>
              </tr>
              
              <tr>
                <th style='font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#f0f0f0;border-top-width:1px;border-bottom-width:1px;vertical-align:top;text-align: center;' colspan='2'>
                  Mensagem recebida de {$recebenome}, via formulário do site.
                </th>
              </tr>
              
              <tr>";
    foreach ($post as $key => $value):
      $corpo .= "<tr>
              <td style='font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-color:#ccc;background-color:#f9f9f9;border-top-width:1px;border-bottom-width:1px;vertical-align:top;border-right:1px solid #ccc;'>
                <b>" . strtoupper(str_replace(array('_', '-'), ' ', $key)) . ": </b>
              </td>
              <td style='font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#f9f9f9;border-top-width:1px;border-bottom-width:1px;vertical-align:top'>
                {$value}
              </td>
              </tr>";
    endforeach;
    $corpo .= "</tr>   
              <tr>
                <td style='text-align:center;font-family:Arial, sans-serif;font-size:9px;padding:10px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#fff;border-top-width:1px;border-bottom-width:1px;text-align:center;vertical-align:top' colspan='2'>
                  Mensagem automática enviada por - {$nomeSite} em " . date('d/m/Y H:i:s') . "
                </td>
              </tr>
              <tr>
                <td style='text-align:center;font-family:Arial, sans-serif;font-size:9px;padding:10px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#fff;border-top-width:1px;border-bottom-width:1px;text-align:center;vertical-align:top' colspan='2'>
                  <a href='{$url}' title='{$nomeSite}'>{$url}</a>
                </td>
              </tr>
            </table>";

// ENVIO EMPRESA
    $mail->From = $EMAIL; // Remetente
    $mail->FromName = $post['nome']; // Remetente nome
    $mail->Sender = $EMAIL; // Seu e-mail

    $mail->AddAddress($emailContato, $EMPRESA); // Destinatário principal
    //Se houver anexo
    if (isset($file) && !empty($file)):
      $mail->AddAttachment($file['tmp_name'], $file['name']); // Anexo
    endif;
    //$mail->AddCC('adm@site.com.br', 'Teste'); // Copia
    //$mail->AddBCC('fulano@dominio.com.br', 'Fulano da Silva'); // Cópia Oculta
    $mail->AddReplyTo($post['email'], $post['nome']); // Reply-to
    $mail->Subject = $EMPRESA . ': Contato pelo site'; // Assunto da mensagem
    $mail->Body = $corpo; // corpo da mensagem
    $mail->Send(); // Enviando o e-mail
    $mail->ClearAllRecipients(); // Limpando os destinatários
    $mail->ClearAttachments(); // Limpando anexos
    
    // ENVIO USUÁRIO
    $mail->From = $recebemail; // Remetente
    $mail->FromName = $EMPRESA; // Remetente nome
    $mail->Sender = $EMAIL; // Seu e-mail
    $mail->AddAddress($post['email'], $post['nome']); // Destinatário principal
    //Se houver anexo
    if (isset($file) && !empty($file)):
      $mail->AddAttachment($file['tmp_name'], $file['name']); // Anexo
    endif;
    $mail->Subject = $EMPRESA . ': Recebemos sua mensagem'; // Assunto da mensagem
    $mail->Body = $corpo; // corpo da mensagem
    $enviado = $mail->Send();
    $mail->Send(); // Enviando o e-mail
    $mail->ClearAllRecipients(); // Limpando os destinatários
    $mail->ClearAttachments(); // Limpando anexos

    include ('inc/insercaoDeLeads.php');


    if ($enviado):
     echo '<script>'
       . '$(function () {';
       echo 'swal({
             title: "Tudo certo!",
             text: "Obrigado por entrar em contato, sua mensagem foi enviada com sucesso",
             type: "success",
             showCancelButton: false,
             confirmButtonClass: "btn-success",
             confirmButtonText: "Ok",
             closeOnConfirm: true
           }, function () {
             location.href = "' . $url . 'obrigado";            
           });';
       echo '});'
       . '</script>';
    else:
      echo '<script>'
      . '$(function () {';
      echo 'swal("Opsss!", "Desculpe, mas houve um erro ao enviar a mensagem, por favor tente novamente.", "error");';
      echo '});'
      . '</script>';
    endif;

  else:
    echo '<script>'
    . '$(function () {';
    echo 'swal("Opsss!", "Desculpe, mas não foi possível verificar o reCaptcha, tente novamente.", "error");';
    echo '});'
    . '</script>';
    
  endif;

else:

  echo '<script>'
  . '$(function () {';
  echo 'swal("Opsss!", "Confirme que não é um robô e marque o reCaptcha.", "error");';
  echo '});'
  . '</script>';
  
endif;
