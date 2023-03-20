<?php


require_once "database.php";

// --- Initial Test Code ------------------------------------------------------------------------

if (isset($_GET['device']) && $_GET['device'] == 'motor')
{
    error_log("Show me a database update");

    if(isset($_GET['action']) && $_GET['action'] == 'GoBrr')
    {
        $randomNumber = random_int(0, 10);
        $query = "UPDATE Motor";
        $query .= " SET Operate = '$randomNumber'";
        

        $results = mysqlNonQuery( $query );
    }
}

if (isset($_GET))
{
    error_log("Basic GET request");
}

error_log(json_encode(($_GET)));

// --- PICO Webservice -----------------------------------------------------------------------

// The webservice for the Pico will mostly involve regularly querying the database to 
// determing if any user setting has been changed, and setting control parameters back 
// to the  resting state. If the Pico is in automatic mode it will have no need to 
// interact with database at all, other than logging data

// Pico Check In

// Pico Control Field Resets

// Exterior Light Intensity Log

// Exterior Light Temperature Log

// Interior Light Intensity Log

// Interior Light Intensity Log

// Curtain Position Log


// --- WEBSITE Webservice --------------------------------------------------------------------

// The webservice for the website will be blind to the mode of the system--whether it's
// automatic or manual--it takes requests for changes from the website and posts those 
// changes up to the database

// Motor 

// LED


?>