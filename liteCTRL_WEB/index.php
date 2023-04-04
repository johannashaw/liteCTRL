<?php

require_once "validate.php";

// check for an active
// session by checking for a session variable called username with an assigned user name. If the
// username is not set, redirect the user to the login.php page. 

// if (!isset($_SESSION['username']))
// {
//     header("Location: login.php");
//     die();
// }

// This is how we redirect to pages 
//header("Location: index.php");

session_unset();

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="./style.css" rel="stylesheet" type="text/css"/>
    <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'></script>
    <script src="./litectrl.js"></script>
    <title>liteCTRL</title>
</head>
<body>
    <div id="mainGrid">
        <div id="header">liteCTRL Panel</div>
            <div id="automaticMenu">
                <div class="twoSpan">Automatic</div>
                <div class="leftMenu">Intensity</div><div class="rightMenu"><input id="intensity" max="100" min="0" type="text"></div>
                <div class="leftMenu">Temperature</div><div class="rightMenu"><input id="temperature" max="100" min="0" type="text"></div>
            </div>

            <div id="manualMenu">
                <div class="twoSpan">Manual</div>
                <div class="leftMenu">Curtain</div><div class="rightMenu"><input id="curtain" max="100" min="0" type="range"></div>
                <div class="leftMenu">
                    <label for="red">Colour</label>
                </div>
                <div class="rightMenu ">
                    <input id="colour" type="color" name="blue">
                </div>
            </div>

        
    </div>
    <footer><span> © liteCTRL ©</span>
        <br>
        <script>document.write('Last modified: ' + document.lastModified);</script>
</body>
</html>

