<?php
$h1     = 'Obrigado';
$texto = "Obrigado por entrar em contato, nossa equipe responderá o mais rápido possível";

$title  = 'Entre em Contato';
$desc   = 'Obrigado - Entre em contato e envie sua mensagem pelo formulário e logo entraremos em contato. Qualquer dúvida estamos a disposição pelo email ou telefone';
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
  <main>
    <div class="content">
      <section>
        <?= $caminhoBread ?>
        <div class="container contact">
          <div class="wrapper">
            <h2><?=$h1?>!</h2>
            <h3><?=$texto?></h3>
            <br>
            <a href="<?=$url?>"><p class="txtcenter">Continuar navegando no site</p></a>
            <br>
          </div>
        </div>
    </section>
  </div>
</main>


<?php include('inc/footer.php'); ?>
</body>
</html>