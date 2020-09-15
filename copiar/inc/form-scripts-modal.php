<!--SweetAlert Modal-->
<style>
	<? include('js/sweetalert/css/sweetalert.css'); ?>
</style>
<!-- <script src="<?= $url; ?>js/sweetalert/js/sweetalert.min.js"></script> -->
<script>
	<?php include 'js/sweetalert/js/sweetalert.min.js'; ?>
</script>
<!--/SweetAlert Modal-->
<!--Máscara dos campos-->
<!-- <script src="<?= $url; ?>js/maskinput.js"></script> -->
<script>
	<?php include 'js/maskinput.js'; ?>
</script>
<script>
$(function () {
$('input[name="telefone"]').mask('(99) 99999-9999');
});
</script>