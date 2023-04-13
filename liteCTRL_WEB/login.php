<?php

require_once "validate.php";

/*  If the $_POST submit has been created and is Login, ensure the username and password are not 
*   empty strings, then cleanse them of potential html tags and external whitespace, dump all of that 
*   into a key/value array, and toss that array to the Validate function to check legitimacy of
*   username and password
*/



if(isset($_POST['submit']) && $_POST["submit"] == "Login"
    && isset($_POST["username"]) && strlen($_POST["username"]) > 0
    && isset($_POST['password']) && strlen($_POST["password"]) > 0)
    {
        error_log("In login block");

        $info = array();
        $info['username'] = strip_tags( trim($_POST["username"]) );
        $info['password'] = strip_tags( trim($_POST["password"]) );
        $info['response'] = "";
        $info['status'] = false;

        $info = Validate($info);

        $_SESSION['response'] = $info['response'];

        error_log($_SESSION['response']);

        // if status returns as true, we redirect to the index page
        if ($info['status'])
        {
            error_log("In info status block");
            $_SESSION['username'] = $info['username'];
            header("Location: index.php");
            die();
        }

        
    }


?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="./login.css" rel="stylesheet" type="text/css"/>
    <link rel="shortcut icon" href="sun_moon.png?v=2" type="image/x-icon">
    <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'></script>
    <!-- Login doesn't seem to need javascript, and link was triggering mode functions that were 
        reactivating modes -->
    <!-- <script src="./litectrl.js"></script> -->
    <title>liteCTRL</title>
</head>
<body>
    <div id="login">
        <div class="twoSpan brightText">Authenticate</div>
        <form id="login" class="twoSpan" method="post" action="<?php echo $_SERVER['PHP_SELF'];?>">
            <div class="leftMenu brightText">Username</div><div class="rightMenu"><input name="username" type="text"></div>
            <div class="leftMenu brightText">Password</div><div class="rightMenu"><input name="password" type="password"></div>
            <input id="submit" type="submit" name="submit" value="Login" class="twoSpan">
        </form>
    </div>
    <div id="mainGrid">
        <div id="header">liteCTRL Panel</div>
            <div id="automaticMenu">
                <div class="twoSpan">Automatic</div>
                <div class="leftMenu">Intensity</div><div class="rightMenu"><input disabled id="intensity" max="100" min="0" type="text"></div>
                <div class="leftMenu">Temperature</div><div class="rightMenu"><input disabled id="temperature" max="100" min="0" type="text"></div>
            </div>

            <div id="manualMenu">
                <div class="twoSpan">Custom</div>
                <div class="leftMenu">Curtain</div><div class="rightMenu"><input disabled id="curtain" max="100" min="0" type="range"></div>
                <div class="leftMenu">
                    <label for="red">Colour</label>
                </div>
                <div class="rightMenu">
                    <input disabled id="colour" type="color" name="blue">
                </div>
            </div>

        
    </div>
    <footer><span> © liteCTRL ©</span>
        <br>
        <script>document.write('Last modified: ' + document.lastModified);</script>
</body>
</html>

