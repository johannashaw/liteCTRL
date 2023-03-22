<?php

require_once "database.php";


// --- PICO Webservice -----------------------------------------------------------------------

// The webservice for the Pico will mostly involve regularly querying the database to 
// determing if any user setting has been changed, and setting control parameters back 
// to the resting state. If the Pico is in automatic mode it will have no need to 
// interact with database at all, other than logging data

// Pico Check In
// Query the database control fields to determine if user has indicated any operations

if(isset($_GET["CheckIn"]))
{
    CheckIn();
}

function CheckIn()
{
    // $query = "SELECT *";
    // $query .= " FROM MotorControl";

    // $results = mySQLQuery( $query );

    // if ($results)
    // {
    //     while ( $row = $results->fetch_assoc())
    //     {
    //         $returnArray[] = $row;
    //     }

    //     echo json_encode($returnArray);
    // }
    // else
    // {
    //     echo "GetData Error";
    // }
}

// Pico Control Field Resets

if(isset($_GET["Reset"]))
{
    Reset();
}

function Reset()
{

}

// Log Data
// Hourly logging of data to database, including:
// Exterior Light Intensity
// Exterior Light Temperature
// Interior Light Intensity
// Interior Light Temperature
// Curtain Position

if(isset($_GET["LogData"]))
{
    LogData();
}

function LogData()
{

}



// --- WEBSITE Webservice --------------------------------------------------------------------

// The webservice for the website will be blind to the mode of the system--whether it's
// automatic or manual--it takes requests for changes from the website and posts those 
// changes up to the database

// Motor 

// LED




?>