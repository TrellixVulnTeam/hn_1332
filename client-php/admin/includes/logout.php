<?php
session_start();
include("config.php");
$cmp_pass[] = md5("$pulse_pass");

if(in_array($_SESSION['mpass_pass'],$cmp_pass)){
	session_destroy();
}
header("Location: ../index.php");
?> 


