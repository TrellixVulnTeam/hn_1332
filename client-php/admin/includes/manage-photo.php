<div class="left-pad">
	<a href="index.php?p=choose-img" class="top-btn"><?php echo $lang_gal_upload; ?></a>
	&nbsp;
	<a target="_blank" href="includes/gal-preview.php" class="top-btn"><?php echo $lang_gal_preview; ?> &rarr;</a>            
</div>

<?php 
     
    $directory = ROOTPATH . "/data/img/gallery/"; 

    $images = array();
    if($image1 = glob($directory."/*.jpg")) $images = $image1;
    if($image2 = glob($directory."/*.jpeg")) $images = array_merge($images,$image2);
    if($image3 = glob($directory."/*.JPG")) $images = array_merge($images,$image3);
    if($image4 = glob($directory."/*.JPEG")) $images = array_merge($images,$image4);
    if($image5 = glob($directory."/*.gif")) $images = array_merge($images,$image5);

    array_multisort(array_map('filemtime', $images), SORT_DESC, $images);  

    $nb = 1;
    if($images) {
        foreach($images as $image) {

            $nb++;
            $imgs[$nb] = basename($image);
					
            global $lang_gal_delete;
					
            echo '<div class="thumb">';
            echo '<a href="data/img/gallery/'.basename($image).'" id="lightbox" rel="lightbox-set">';
            echo '<img src="data/img/gallery/'.basename($image).'"  class="thumb-pic"/>';
            echo '<img src="img/mag-glass.png" class="mag-glass" />';
            echo '</a>';
            echo "<br><a href=\"index.php?p=del-img&f=". $nb ."\" class=\"del-img\">$lang_gal_delete</a>";
            echo "</div>"; 

            $count++;

        }
        $_SESSION["images"] = $imgs;
    } else {
        echo "<p class=\"created\">". $lang_gal_empty ."</p>";
    
}
?>	

<div style="clear:both"></div>	 
	 	
<div class="howto">
	<a href="javascript:doMenu('main');" id=xmain><?php echo $lang_embed; ?></a>
	<div id="main" style="display:none;">
	<p><?php echo $lang_embed_desc; ?></p>
	<input value='&lt;?php include("<?php echo ROOTPATH; ?>/includes/gallery.php"); ?&gt;' onClick="select_all(this)" >             
	</div>
</div>