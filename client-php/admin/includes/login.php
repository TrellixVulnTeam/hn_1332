<?php
session_start();
include_once("config.php");
$max_session_time = 36000;
$cmp_pass = Array();
$cmp_pass[] = md5($pulse_pass);
$max_attempts = 10;
$session_expires = $_SESSION["mpass_session_expires"];
$max_attempts++;

if(!empty($_POST["mpass_pass"]))
{
	$_SESSION["mpass_pass"] = md5($_POST["mpass_pass"]);
}

if(empty($_SESSION["mpass_attempts"]))
{
	$_SESSION["mpass_attempts"] = 0;
}

if(($max_session_time>0 && !empty($session_expires) && time()>$session_expires) || empty($_SESSION["mpass_pass"]) || !in_array($_SESSION["mpass_pass"],$cmp_pass))
{
	if(!in_array($_SESSION["mpass_pass"],$cmp_pass))
	{
		$_SESSION["mpass_attempts"]++;
	}
	
	if($max_attempts>1 && $_SESSION["mpass_attempts"]>=$max_attempts)
	{
		exit($lang_login_fail);
	}

	$_SESSION["mpass_session_expires"] = "";

?>
<!DOCTYPE html>
<html>
<head>
    <title><?php echo $lang_page_title; ?></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link rel="stylesheet" type="text/css" href="css/styles.css" media="all">
</head>

<body id="login-page" onload="document.login.mpass_pass.focus()">
    <div id="top">
    <form name="login" action="<?php htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post" id="login">
    	<img src="img/new-logo.png" alt="Pulse CMS">
    	<?php
			if (!empty($_POST["mpass_pass"]) && !in_array(md5($_POST["mpass_pass"]), $cmp_pass))
			echo "<p class=\"errorMsg\">$lang_login_incorrect</p>"; ?>
        <label for="password"><?php echo $lang_login_login_label; ?></label> 
        <input type="password" size="27" name="mpass_pass"> 
        <button type="submit" class="log-btn"><?php echo $lang_login_login_button; ?></button>
    </form>
    </div>
    <!-- Pulse Basic -->
</body>
</html>
<?php 
exit();
}
$_SESSION["mpass_attempts"] = 0;
$_SESSION["mpass_session_expires"] = time()+$max_session_time;
?>