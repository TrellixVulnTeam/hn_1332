<?php 
include('config.php'); 
include_once("path.php"); 
error_reporting(0);
?>

<script type="text/javascript" src="http://<?php echo $_SERVER['HTTP_HOST'] ?>/<?php echo $pulse_dir?>/plugins/jquery/jquery-1.5.min.js"></script>
<script type="text/javascript" src="http://<?php echo $_SERVER['HTTP_HOST'] ?>/<?php echo $pulse_dir?>/plugins/slimbox/js/slimbox2.js"></script>
<link rel="stylesheet" href="http://<?php echo $_SERVER['HTTP_HOST'] ?>/<?php echo $pulse_dir?>/plugins/slimbox/css/slimbox2.css" type="text/css" media="screen" />

<style type="text/css">
.gallery img {
padding:0;
width:80px;
height:80px;
margin:5px;
float:left;
border:0;
-webkit-box-shadow:1px 1px 3px rgba(0, 0, 0, 0.3);
-moz-box-shadow:1px 1px 3px rgba(0, 0, 0, 0.3);
-box-shadow:1px 1px 3px rgba(0, 0, 0, 0.3);
}

.gallery li {
padding:0;
margin:0;
list-style-type:none;
}

.gallery img:hover {
-webkit-transform: scale(1.1);
-moz-transform: scale(1.1);
transform: scale(1.1);
-webkit-box-shadow:4px 4px 10px rgba(0, 0, 0, 0.3);
-moz-box-shadow:4px 4px 10px rgba(0, 0, 0, 0.3);
-box-shadow:4px 4px 10px rgba(0, 0, 0, 0.3);
}
</style>

<div class="gallery">

<?php 
$directory = ROOTPATH . "/data/img/gallery/"; 

$images = array();
if($image1 = glob($directory."/*.jpg")) $images = $image1;
if($image2 = glob($directory."/*.jpeg")) $images = array_merge($images,$image2);
if($image3 = glob($directory."/*.JPG")) $images = array_merge($images,$image3);
if($image4 = glob($directory."/*.JPEG")) $images = array_merge($images,$image4);
if($image5 = glob($directory."/*.gif")) $images = array_merge($images,$image5);

array_multisort(array_map('filemtime', $images), SORT_DESC, $images);

if (empty($max_img)) {
    $max_img = "50";
}

array_splice($images, $max_img); 

foreach($images as $image) {
echo '<a href="http://'.$_SERVER['HTTP_HOST'].'/'.$pulse_dir.'/data/img/gallery/'.basename($image).'" rel="lightbox-set" >' . "\n";
echo '<img src="http://'.$_SERVER['HTTP_HOST'].'/'.$pulse_dir.'/data/img/gallery/'.basename($image).'" alt="" />';
echo '</a>' . "\n\n";
}
?>

</div>

<div style="clear:both"></div>