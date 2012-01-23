<?php

$domain = $_SERVER['HTTP_HOST'];

$timestamp_old = time() - (60*60);

// edit/save the block content
if(isset($_SESSION["token"]) && isset($_SESSION["token_time"]) && isset($_POST["token"]) && $_SESSION["token"] == $_POST["token"] && isset($_POST["filename"])){
	
	if($_SESSION["token_time"] >= $timestamp_old){
	
		$id = stripslashes($_POST["filename"]);
		$fname = $_SESSION["blocks"][$id];

		$fname = strip_tags($fname);
		$fname = str_replace("..", "", $fname);
		$fname = ltrim($fname, "/");

		$block = stripslashes(str_replace(array("<?","?>"), array("",""), $_POST["block"]));
		
		if($_POST["move"]){
			$fmove = str_replace("..", "", $_POST["move"]);
			$info = pathinfo($fname);
			$fname = "data/blocks". $fmove.$info["basename"];
			$fp = @fopen($fname, "w");
			if ($fp) {
				fwrite($fp, $block);
				fclose($fp);
				if(unlink($_SESSION["blocks"][$id])){
					$_SESSION["blocks"][$id] = $fname;
				}
			}		
		}else{
		 	$fp = @fopen($fname, "w");
		 	if ($fp) {
				fwrite($fp, $block);
				fclose($fp);
			}		
		}
		
		unset($_SESSION["token"]);	
		unset($_SESSION["token_time"]);
	}
}

// read the block content
if (isset($_GET["f"]) && isset($_SESSION["blocks"])) 
	$id = stripslashes(htmlentities($_GET["f"]));
	$fname = $_SESSION["blocks"][$id];
	$fname = str_replace("..", "", $fname);
	$fname = ltrim($fname, "/");
	$folders = strtr($_GET["d"], "../","/");
	if (file_exists($fname)) { 
		$fp = @fopen($fname, "r");
		if (filesize($fname) !== 0) 
			$loadblock = fread($fp, filesize($fname));
			$loadblock = htmlspecialchars($loadblock);
			fclose($fp);
	
	if(empty($_SESSION["token"]) || $_SESSION["token_time"] <= $timestamp_old){
		$_SESSION["token"] = md5(uniqid(rand(), TRUE));	
		$_SESSION["token_time"] = time();
	}				
?>
	
	 <div class="breadcrumb-fold"><a href="."><?php echo $lang_blocks_home; ?></a>
	 <?php if($folders) { ?>
	  > <a href="index.php?p=blocks&d=<?php echo $folders; ?>"><?php echo $folders; ?></a>
	 <?php }?>
	  > 
	 <?php  $info = pathinfo($fname); echo $info["basename"]; 
	 	if($folders){
	 ?> 
		<a class="block-delete" href="index.php?p=del-block&f=<?php echo $id; ?>&d=<?php echo $folders; ?>" title="<?php echo $lang_blocks_delblock_title; ?>" ><?php echo $lang_blocks_delblock; ?></a>
	<?php }else{ ?>
		<a class="block-delete" href="index.php?p=del-block&f=<?php echo $id; ?>" title="<?php echo $lang_blocks_delblock_title; ?>" ><?php echo $lang_blocks_delblock; ?></a>
	<?php 
		}
	?>
	 </div>					
		<form class="editor" method="post" action="">	
		<input type="hidden" name="filename" value="<?php echo $id; ?>" />
		<input type="hidden" name="token" value="<?php echo $_SESSION["token"] ?>" />
		<textarea class="block_editor" id="area2" name="block" cols="90" rows="20"><?php echo $loadblock; ?></textarea><br>
		<script type="text/javascript">
			
	CKEDITOR.replace( 'area2', {
				
		filebrowserImageBrowseUrl : 'plugins/ckeditor/filemanager/browser/default/browser.html?Type=Image&Connector=http://<?php echo $domain."/".$pulse_dir; ?>/plugins/ckeditor/filemanager/connectors/php/connector.php'
			
		});

	</script>

	<button type="submit" class="create-btn"><?php echo $lang_blocks_save; ?></button>
	
	</form>
		
<div class="howto">
	<a href="javascript:doMenu('main');" id=xmain><?php echo $lang_embed; ?></a>
	<div id="main" style="display:none;">
	<p><?php echo $lang_embed_desc; ?></p>
	<input value='&lt;?php include("<?php echo ROOTPATH; ?>/<?php echo $fname; ?>"); ?&gt;' onclick="select_all(this)" > 
	</div>
</div>	          
                      
<?php 
}else{
?>
<div style="margin:0 0 0 15px;"><span class="errorMsg"><?php echo $lang_blocks_cant_find_block; ?></span></div>
<?php } ?>