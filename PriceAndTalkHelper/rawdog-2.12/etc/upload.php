<?php 
/*** 
    this is a simple and complete function and 
    the easyest way i have found to allow you 
    to add an image to a form that the user can 
    verify before submiting 

    if the user do not want this image and change 
    his mind he can reupload a new image and we 
    will delete the last 

    i have added the debug if !move_uploaded_file 
    so you can verify the result with your 
    directory and you can use this function to 
    destroy the last upload without uploading 
    again if you want too, just add a value... 
***/ 

function upload_back() { global $globals; 

/*** 
    1rst set the images dir and declare a files 
    array we will have to loop the images 
    directory to write a new name for our picture 
***/ 

  $uploaddir = '../rss_feed/'; $dir = opendir($uploaddir); 
  $files = array(); 

/*** 
    if we are on a form who allow to reedit the 
    posted vars we can save the image previously 
    uploaded if the previous upload was successfull. 
    so declare that value into a global var, we 
    will rewrite that value in a hidden input later 
    to post it again if we do not need to rewrite 
    the image after the new upload and just... save 
    the value... 
***/ 

  if(!empty($_POST['attachment_loos'])) { $globals['attachment'] = $_POST['attachment_loos']; } 

/*** 
    now verify if the file exists, just verify 
    if the 1rst array is not empty. else you 
    can do what you want, that form allows to 
    use a multipart form, for exemple for a 
    topic on a forum, and then to post an 
    attachment with all our other values 
***/ 

  if(isset($_FILES['attachment']) && !empty($_FILES['attachment']['name'])) { 

/*** 
    now verify the mime, i did not find 
    something more easy than verify the 
    'image/' ty^pe. if wrong tell it! 
***/ 

/***
    if(!eregi('xml/', $_FILES['attachment']['type'])) { 

      echo 'The uploaded file is not an xml please upload a valide file!\n' + $_FILES['attachment']['name'] + '.' + $_FILES['attachment']['type']; 

    } else { 
***/
/*** 
    else we must loop our upload folder to find 
    the last entry the count will tell us and will 
    be used to declare the new name of the new 
    image. we do not want to rewrite a previously 
    uploaded image 
***/ 

//        while($file = readdir($dir)) { array_push($files,"$file"); echo $file; } closedir($dir); 

/*** 
    now just rewrite the name of our uploaded file 
    with the count and the extension, strrchr will 
    return us the needle for the extension 
***/ 

//        $_FILES['attachment']['name'] = ceil(count($files)+'1').''.strrchr($_FILES['attachment']['name'], '.'); 
        $uploadfile = $uploaddir . basename($_FILES['attachment']['name']); 

/*** 
    do same for the last uploaded file, just build 
    it if we have a previously uploaded file 
***/ 

//        $previousToDestroy = empty($globals['attachment']) && !empty($_FILES['attachment']['name']) ? '' : $uploaddir . $files[ceil(count($files)-'1')]; 

// now verify if file was successfully uploaded 

      if(!move_uploaded_file($_FILES['attachment']['tmp_name'], $uploadfile)) { 

echo '<pre> 
Your file was not uploaded please try again 
here are your debug informations: 
'.print_r($_FILES) .' 
</pre>'; 

      } else { 

          echo 'image successfully uploaded!'; 

      } 

/*** 
    and reset the globals vars if we maybe want to 
    reedit the form: first the new image, second 
    delete the previous.... 
***/ 

        $globals['attachment'] = $_FILES['attachment']['name']; 
        if(!empty($previousToDestroy)) { unlink($previousToDestroy); } 

    } 

  } 
/***
}
***/ 

upload_back(); 

/*** 
    now the form if you need it (with the global...): 

    just add the hidden input when you write your 
    preview script and... in the original form but! 
    if you have send a value to advert your script 
    than we are remaking the form. for exemple with a 
    hidden input with "reedit" as value  or with a 
    $_GET method who can verify that condition 
***/ 

echo '<form action="" method="post" enctype="multipart/form-data"> 

  <input type="file" name="attachment" name="attachment"></input> 
  <input type="hidden" name="attachment_loos" name="attachment_loos" value="', $globals['attachment'] ,'"></input> 

  <input type="submit" value="submit"></input> 

</form>'; 
?>