<div class="left-pad">
	<a href="index.php?p=backup" class="top-btn"><?php echo $lang_backup_now; ?></a>            
</div>	
	
<div class="backup-list">
	
	<?php 
	
	$files = glob("data/backups/*");
	if( $files) {
	foreach ($files as $file)  if (!is_dir($file)) {
	
	?>
	<div class="zips">
		 <a href="<?php echo $file; ?>">
		 <?php $file = preg_replace("/\\.[^.\\s]{3,4}$/", "", $file);
		echo basename($file);?></a>
	</div>
	<?php }
	} 
	$_SESSION["backups"] = $backups;
	?>

</div>