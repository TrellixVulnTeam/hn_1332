<p class="left-pad"><b><?php echo $lang_gal_select; ?></b></p>

<div class="upload">		
	<form action="index.php?p=upload-img" method="post" enctype="multipart/form-data">
	<input type="file" name="file" id="file" />
	<button type="submit" class="create-btn"><?php echo $lang_gal_upload_button; ?></button>
	</form>
</div>

<p class="left-pad"><?php echo $lang_gal_max; ?></p>