<div class="left-pad">
<?php 
	
	if(!empty($_GET["f"])){
		
		$id = htmlentities($_GET["f"]);
		$filename = $_SESSION["images"][$id];
	
		$upload_dir = "./data/img/gallery/";
		$file_path = $upload_dir . $filename;
		if(is_file($file_path)) {

			if(isset($_SESSION["token"]) && isset($_SESSION["token_time"]) && isset($_POST["token"]) && $_SESSION["token"] == $_POST["token"]){
				$timestamp_old = time() - (15*60);
			
				if($_SESSION["token_time"] >= $timestamp_old){
					unlink($file_path);
					echo "<p>$lang_gal_file <b>" . $filename . "</b> $lang_gal_file_deleted</p>";
					echo "<p>$lang_gal_image_manager</p>";
				}else{
					echo "<p class=\"errorMsg created\">$lang_gal_session_expired</p>";
				}			
			}else{
				$token = md5(uniqid(rand(), TRUE));
				$_SESSION["token"] = $token;
				$_SESSION["token_time"] = time();
				echo "<p>$lang_gal_sure_delete_file <b>" . $filename . "</b>?</p>";
				echo "<form action=\"index.php?p=del-img&f=$id\" method=\"post\">";
				echo "<p><input type=\"hidden\" name=\"token\" value=\"$token\" />";
				echo "<button value=\"Yes\" type=\"submit\" class=\"top-btn\">$lang_yes</button>";
				echo "&nbsp;&nbsp;&nbsp;<a href=\"index.php?p=manage-photo\" class=\"top-btn\">$lang_cancel</a>";
				echo "</form>";
			
			}		
		}else{
			echo "<p class=\"errorMsg\">$lang_gal_cant_find_file</p>";
			echo "<p>$lang_gal_image_manager</p>";
		}
			
	}else{
		echo "<p class=\"errorMsg\">$lang_gal_cant_find_file</p>";
		echo "<p>$lang_gal_image_manager</p>";
	}
?>
</div>