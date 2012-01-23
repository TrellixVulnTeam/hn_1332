<?php
include "archive.php";
$today = date("m.j.y-gi");
$test = new zip_file("./data/backups/" . $today . ".zip"); 
$test->set_options(array('inmemory' => 0, 'recurse' => 1, 'storepaths' => 1));
$test->add_files("./data/blocks/*.*");
$test->add_files("./data/blog/*.*");
$test->add_files("./data/img/*.*");
$test->create_archive();
print "<p class=\"complete\"><b>$lang_backup_complete</b></p>";
?>

<?php $_SESSION["backups"] = $backups; ?>