<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="./login.css" rel="stylesheet" type="text/css"/>
    <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'></script>
    <script src="./litectrl.js"></script>
    <title>liteCTRL</title>
</head>
<body>
    <div id="login">
        <div class="twoSpan">Authenticate</div>
        <div class="leftMenu">Username</div><div class="rightMenu"><input type="text"></div>
        <div class="leftMenu">Password</div><div class="rightMenu"><input type="text"></div>
    </div>
    <div id="mainGrid">
        <div id="header">liteCTRL Panel</div>
            <div id="automaticMenu">
                <div class="twoSpan">Automatic</div>
                <div class="leftMenu">Intensity</div><div class="rightMenu"><input disabled id="intensity" max="100" min="0" type="text"></div>
                <div class="leftMenu">Temperature</div><div class="rightMenu"><input disabled id="temperature" max="100" min="0" type="text"></div>
            </div>

            <div id="manualMenu">
                <div class="twoSpan">Manual</div>
                <div class="leftMenu">Position</div><div class="rightMenu"><input disabled id="curtain" max="100" min="0" type="range"></div>
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

