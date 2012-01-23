<!DOCTYPE html>
<html>
<head>
	<title><?php echo $lang_page_title; ?></title>
	<meta charset="utf-8" />
	
	<link rel="stylesheet" href="css/styles.css" media="all" />
	<link rel="stylesheet" href="plugins/slimbox/css/slimbox2.css" media="all" />
	
	<script type="text/javascript" src="plugins/ckeditor/ckeditor.js"></script> 
	<script type="text/javascript" src="plugins/jquery/jquery-1.5.min.js"></script>
	<script type="text/javascript" src="plugins/slimbox/js/slimbox2.js"></script>
	
	<script type="text/javascript"> function doMenu(item) { obj=document.getElementById(item); col=document.getElementById("x" + item); if (obj.style.display=="none") { obj.style.display="block"; col.innerHTML="<?php echo $lang_embed; ?>"; } else { obj.style.display="none"; col.innerHTML="<?php echo $lang_embed; ?>"; } } 
	</script>
	
</head>
	
<body>	

<script type="text/javascript"> 
function select_all(obj) 
{ var text_val=eval(obj); 
text_val.select(); } 
</script>
		
	<div class="header">
	<div class="inner">		
	<a href="index.php"><img src="img/new-logo.png" alt="Pulse CMS" border="0"/></a>		
	<div class="clear"></div>	
	
	<ul class="nav">
		<li>
		<a <?php if ($current=="blocks") 
		echo " class=\"current\""; ?> href="index.php?p=blocks" ><?php echo $lang_nav_blocks; ?></a></li>
		
		<li>
		<a <?php if ($current=="images") 
		echo " class=\"current\""; ?> href="index.php?p=manage-photo"><?php echo $lang_nav_galleries; ?></a></li>
		
		<li>
		<a <?php if ($current=="backup") 
		echo " class=\"current\""; ?> href="index.php?p=list-backups"><?php echo $lang_nav_backup; ?></a></li>

		<li>
		<a href="includes/logout.php" ><?php echo $lang_nav_logout; ?></a></li>
	</ul>

<div class="clear"></div>
	
</div></div>
		
<div class="content">
