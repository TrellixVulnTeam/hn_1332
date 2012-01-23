<?php
if(isset($_SESSION["token"]) && isset($_SESSION["token_time"]) && isset($_POST["token"]) && $_SESSION["token"] == $_POST["token"] && !empty($_POST['blockname'])){
	$timestamp_old = time() - (15*60);
		
	if($_SESSION["token_time"] >= $timestamp_old){
		
		@$filename = strip_tags($_POST['blockname']) . ".html";
        $blockname = str_replace(' ', '-', $filename);
		
		if(!empty($_GET["d"] )) {
			$folders = strtr($_GET["d"], "../","/");
			$block_total = "data/blocks/". $folders ."/". $blockname;
		}else{
			$block_total = "data/blocks/" . $blockname;
		}
		$block_handle = fopen($block_total, 'w') or die("{$blockname} $lang_blocks_not_created");
		fclose($block_handle);
		$_SESSION["blocks"]["new"] = $block_total;
		if($folders) {
			echo "<p class=\"created\"><b>" . $blockname . "</b> $lang_blocks_was_created <a href=\"index.php?p=blocks&d=". $folders ."\">$lang_blocks_view_created</a></p>";
		}else{
			echo "<p class=\"created\"><b>" . $blockname . "</b> $lang_blocks_was_created <a href=\"index.php?p=blocks\">$lang_blocks_view_created</a></p>";
		}
		unset($_SESSION["token"]);	
		unset($_SESSION["token_time"]);
			
	}else{
		echo "<p class=\"errorMsg created\">$lang_blocks_session_expire</p>";
	}
}

if(empty($_SESSION["token"]) || $_SESSION["token_time"] <= $timestamp_old){
		 $_SESSION["token"] = md5(uniqid(rand(), TRUE));	
		 $_SESSION["token_time"] = time();
}
			
?>		
<div class="create-new">	
	<form action="<?php htmlspecialchars($_SERVER['PHP_SELF']); ?>" method="post" class="create-form">
	<label for="blockname"><?php echo $lang_blocks_blockname; ?></label>
	<input type="text" name="blockname" id="blockname" />
	<input type="hidden" name="token" value="<?php echo $_SESSION["token"] ?>" />
	<input type="submit" value="<?php echo $lang_blocks_create; ?>" class="create-btn"/>				
	</form>
</div><br>
<div style="clear: both;"></div> 

</div>
