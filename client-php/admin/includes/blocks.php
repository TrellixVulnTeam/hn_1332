<?php if($_GET["d"]){ 
		$folders = strtr($_GET["d"], "../","/");
	?>	
		<div class="block-buttons">
		<a href="index.php?p=new-block&d=<?php echo $folders; ?>" class="top-btn"><?php echo $lang_blocks_newblock; ?></a> &nbsp;
		<a href="index.php?p=del-block&d=<?php echo $folders; ?>" class="top-btn"><?php echo $lang_blocks_delfold; ?></a>
		</div>
		<div class="breadcrumb-fold"><a href="."><?php echo $lang_blocks_home; ?></a> > <?php echo $folders; ?> </div>
	<?php }else{ ?>
		<div class="block-buttons">
		<a href="index.php?p=new-block" class="top-btn"><?php echo $lang_blocks_newblock; ?></a> &nbsp;
		</div>
	<?php } ?>     

<?php

function getFiles($folder="") {
	if($folder) {
		$files = glob("data/blocks/". $folder ."/*");
	}else {
		$files =  glob("data/blocks/*");
	}	

	foreach ($files as $file) { 
		if ($file != "." && $file != ".." ) {
			if($folder) {
				$dm[] = $file;;
			}else {
				$dm[] = $file;
			}	
			
		}
	}	
	return $dm;
}

if(!empty($_GET["d"] )) {
	$folders = strtr($_GET["d"], "../","/");
	$files = getFiles($folders);
}else {
	$files = getFiles();
}

if(count($files) >= 1){
	foreach ($files as $file) { 
		$nb++;
		if (!is_dir($file)) {
	?>

		<div class="icon">
		<?php if($folders){ ?>
			<a href="index.php?p=view&f=<?php echo $nb; ?>&d=<?php echo $folders; ?>">
		<?php }else{ ?>
			<a href="index.php?p=view&f=<?php echo $nb; ?>">
		<?php 
			}
			$info = preg_replace("/\\.[^.\\s]{3,4}$/", "", $file);
			echo basename($info);
			$blocks[$nb] = $file; 
			?>
		</a>
	</div>
	<?php 
		}else{
		$file_name =  basename($file);	
	?>	
		<div class="folder">
		<a href="index.php?p=blocks&d=<?php echo $file_name; ?>">
	
	<?php
	
		$blocks[$nb] = $file; 
		echo $file_name;
	?>
		</a>
		</div>
	<?php	
		}
	}
	$_SESSION["blocks"] = $blocks; 
}else{
	echo "<div class=\"left-pad\"><p>$lang_blocks_emptyfold</p></div>";
}	
?>