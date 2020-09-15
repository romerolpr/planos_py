<?php
$h1     = 'Sucesso';
$texto = "Obrigado por entrar em contato, nossa equipe responderá o mais rápido possível";

$title  = 'Entre em Contato';
$desc   = 'Sucesso - Entre em contato e envie sua mensagem pelo formulário e logo entraremos em contato. Qualquer dúvida estamos a disposição pelo email ou telefone';
$key    = 'salgados, máquinas, coxinhas';
$var    = 'Entre em Contato';
include('inc/head.php');
?>
<style>
  .contact {
    display: block;
    padding: 40px 0;
    text-align: center;
  }
</style>
</head>
<body>
<?php include('inc/topo.php'); ?>
<div class="wrapper">
  <main>
    <div class="content">
      <section>
        <?=$caminho?>
         <h1><?=$h1?></h1>
        <div class="container contact">
          
            <h2><?=$h1?>!</h2>
            <h3><?=$texto?></h3>
            <br>
            <a href="<?=$url?>"><p class="txtcenter">Continuar navegando no site</p></a>
            <br>
          </div>
    
    </section>
  </div>
</main>
    </div>

<?php include('inc/footer.php'); ?>
</body>
</html>