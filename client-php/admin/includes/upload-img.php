<div class="left-pad">

<?php
$image = getimagesize($_FILES["file"]["tmp_name"]);

// Allowed file types for upload
$ext = array('jpg','jpeg');

if(($_FILES["file"]["size"] < 160000) && 
(in_array( strtolower(substr(strrchr($_FILES['file']['name'], '.'), 1)), $ext)) && 
(($image[2] == 1 ) || ($image[2] == 2) || ($image[2] == 3))){

	  if ($_FILES["file"]["error"] > 0){
			echo "$lang_gal_file_code " . $_FILES["file"]["error"] . "<br />";
	  }else{
			echo "$lang_gal_file_upload " . $_FILES["file"]["name"] . "<br />";
			echo "$lang_gal_file_type " . $_FILES["file"]["type"] . "<br />";
			echo "$lang_gal_file_size " . ($_FILES["file"]["size"] / 1024) . " Kb<br />";


			if (file_exists("data/img/gallery/" . $_FILES["file"]["name"])){
			  echo $_FILES["file"]["name"] . " $lang_gal_file_exists ";
			}else{
			  move_uploaded_file($_FILES["file"]["tmp_name"],
			  "data/img/gallery/" . $_FILES["file"]["name"]);
			  chmod("data/img/gallery/" . $_FILES["file"]["name"],0774);
			  echo "$lang_gal_file_stored " . "data/img/gallery/" . $_FILES["file"]["name"];
			}
	}
}else{
	echo "<p class=\"errorMsg\">$lang_gal_file_invalid</p>";
}	  
?>

<p><a href="index.php?p=manage-photo"><?php echo $lang_gal_view_images; ?></a></p>
</div>