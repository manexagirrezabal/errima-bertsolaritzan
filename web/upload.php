
<?php
$target_dir = "uploads/";
if(isset($_POST["submit"])) {
    $path = $_FILES["fileToUpload"]["tmp_name"];
    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
    echo "-".$check."-".$check["mime"]."-".mime_content_type($path)."-";
    if (mime_content_type($path) == "text/plain") {
      echo "I'm a text file";
      echo "I'm this file: ".$path;
#      $fh = fopen($path,'r');
#      while ($line = fgets($fh)) {
#   echo($line);
#      }
#      fclose($fh);

      $emaitza=exec('python scriptak/analizatuHainbat.py '.$path);
      echo $emaitza;
    }
}
?>



