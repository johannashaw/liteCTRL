<?php
// This functions file contains all of the helper functions for the other pages

/*
What is a php session?

When you work with an application, you open it, do some changes, and then you close it. 
This is much like a Session. The computer knows who you are. It knows when you start the application 
and when you end. But on the internet there is one problem: the web server does not know who you are 
or what you do, because the HTTP address doesn't maintain state.

Session variables solve this problem by storing user information to be used across 
multiple pages (e.g. username, favorite color, etc). By default, session variables last until 
the user closes the browser.

So; Session variables hold information about one single user, and are 
available to all pages in one application.
*/

session_start();

// An array of key value pairs to be used as valid credential references until we 
// begin using external sources
$userTable = array();
$userTable['Johanna'] = password_hash('puppet', PASSWORD_DEFAULT);


/*****************************
Function Name: Validate
Description: Take the html stripped data from the login page and verify it against
entries in the $userTable array
Parameters: An array
Returns: An array
****************************/
function Validate($cleansedArray)
{
    // brings the $userTable into global scope so the Validate function can access it
    global $userTable;

    foreach ($userTable as $key => $value) {
        // if $cleansedArray username matches value in the $userTable usernames
        if ($key == $cleansedArray['username'])
        {
            // password_verify — Verifies that a password matches a hash
            // this is the counterpart to the password_hash function
            // if $cleansedArray password matches value in the $userTable passwords
            if(password_verify($cleansedArray['password'], $value)) 
            {
                $cleansedArray['response'] = "Successfully logged in as {$cleansedArray['username']}";
                $cleansedArray['status'] = true;

                $_SESSION['username'] = $cleansedArray['username'];

                return $cleansedArray;
            }
            // if password no good, deliver the boot
            else {
                $cleansedArray['response'] = "Login WRONG!!!";
                $cleansedArray['status'] = false;
            }
        }
        // if username no good, also deliver the boot
        else{
            $cleansedArray['response'] = "Login WRONG!!!";
            $cleansedArray['status'] = false;
        }
    }

    // bail out of function, sending validation 'status' = true/false back to the call location
    return $cleansedArray;


}