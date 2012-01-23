<?php
$page = $_REQUEST['p'];

switch ($page) {
	default:
	case "":
		include("includes/blocks.php");
		break;
	
	case $page:
		
		$page = str_replace("/","", $page);
		
		if(file_exists("includes/".$page.".php"))
            include("includes/".$page.".php");
        else
        include("includes/404.php"); 
	
		break;
	}
?>
