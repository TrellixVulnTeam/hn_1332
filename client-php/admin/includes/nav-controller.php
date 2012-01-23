<?php
$page = $_REQUEST['p'];

switch ($page) {
	
	default:
	case "blocks":
	case "view":
	case "new-block":
	$current = "blocks";
	break;
	
	case "manage-gallery":
	case "choose-img":
	case "upload-img":
	case "manage-photo":
	case "new-gallery":
	case "del-img":
	case "del-gal":
	$current = "images";
	break;	
		
	case "list-backups":
	case "backup":
	$current = "backup";
	break;

}
?>