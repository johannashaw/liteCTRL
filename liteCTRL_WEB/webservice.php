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

if(isset($_GET["ResetControls"]))
{
    ResetControls();
}

function ResetControls()
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
// If user has indicated operation that requires motor, post arguments up to the database

function Motor()
{
    error_log(json_encode(($_GET)));
}

// LED
// If user has indicated operation that requires LED, post arguments up to the database

if(isset($_GET["LED"]))
{
    LED();
}

function LED()
{

}

// System Settings
// Storage of webpage user settings so they're not lost upon refresh

// --- Set all inputs from database ----------------------------------------------------------

if(isset($_GET["settings"]))
{
    //error_log("Settings {$_GET["settings"]}");
    GetSettings();
}

function GetSettings()
{
    $returnArray = [];

    // Get Light Intensity
    $query = "SELECT * FROM LightIntensity";
    $results = mysqlQuery( $query );

    if ($results)
    {
        while ( $row = $results->fetch_assoc() )
        {
            $returnArray["LightIntensity"] = $row;
        }
    }

    // Get Light Temperature
    $query = "SELECT * FROM LightTemperature";
    $results = mysqlQuery( $query );

    if ($results)
    {
        while ( $row = $results->fetch_assoc() )
        {
            $returnArray["LightTemperature"] = $row;
        }
    }

    // Get Curtain Position
    $query = "SELECT * FROM CurtainPosition";
    $results = mysqlQuery( $query );

    if ($results)
    {
        while ( $row = $results->fetch_assoc() )
        {
            $returnArray["CurtainPosition"] = $row;
        }
    }

    // Get Light Intensity
    $query = "SELECT * FROM LEDColour";
    $results = mysqlQuery( $query );

    if ($results)
    {
        while ( $row = $results->fetch_assoc() )
        {
            $returnArray["LEDColour"] = $row;
        }
    }

    // Get System Mode
    $query = "SELECT * FROM SystemMode";
    $results = mysqlQuery( $query );

    if ($results)
    {
        while ( $row = $results->fetch_assoc() )
        {
            $returnArray["SystemMode"] = $row;
        }
    }


    echo json_encode($returnArray);
}

// --- System Mode Change -------------------------------------------------------------

if(isset($_GET["systemmode"]))
{
    //error_log("Light Intensity {$_GET["intensity"]}");
    SystemModeDelete();
    SystemModeInsert($_GET["systemmode"]);
}

function SystemModeDelete()
{
    $query = "DELETE FROM SystemMode";

    $results = mySQLNonQuery( $query );

    // I can't echo here, it terminates the server process, equivalent to return in a function
    //echo $results;
}

function SystemModeInsert($value)
{
    error_log("system mode value $value");
    $query = "INSERT INTO `SystemMode` (`Mode`) VALUES ('$value')";

    $results = mySQLNonQuery( $query );

    echo $results;
}

// --- Light Intensity Change --------------------------------------------------------- 
if(isset($_GET["intensity"]))
{
    error_log("Light Intensity {$_GET["intensity"]}");
    LightIntensityDelete();
    LightIntensityInsert($_GET["intensity"]);
}

function LightIntensityDelete()
{
    $query = "DELETE FROM LightIntensity";

    $results = mySQLNonQuery( $query );

    // I can't echo here, it terminates the server process, equivalent to return in a function
    //echo $results;
}

function LightIntensityInsert($value)
{
    $query = "INSERT INTO `LightIntensity`(`Value`) VALUES ($value)";

    $results = mySQLNonQuery( $query );

    echo $results;
}

// --- Light Temperature Change ---------------------------------------------------------
if(isset($_GET["temperature"]))
{
    //error_log("Light Temperature {$_GET["temperature"]}");
    LightTemperatureDelete();
    LightTemperatureInsert($_GET["temperature"]);
}

function LightTemperatureDelete()
{
    $query = "DELETE FROM LightTemperature";

    $results = mySQLNonQuery( $query );

    // I can't echo here, it terminates the server process, equivalent to return in a function
    //echo $results;
}

function LightTemperatureInsert($value)
{
    $query = "INSERT INTO `LightTemperature` (`Value`) VALUES ($value)";

    $results = mySQLNonQuery( $query );

    echo $results;
}

// --- Curtain Position Change -----------------------------------------------------------
if(isset($_GET["curtain"]))
{
    //error_log("Curtain Position {$_GET["curtain"]}");
    CurtainPositionDelete();
    CurtainPositionInsert($_GET["curtain"]);
}

function CurtainPositionDelete()
{
    $query = "DELETE FROM CurtainPosition";

    $results = mySQLNonQuery( $query );

    // I can't echo here, it terminates the server process, equivalent to return in a function
    //echo $results;
}

function CurtainPositionInsert($value)
{
    $query = "INSERT INTO `CurtainPosition` (`Value`) VALUES ($value)";

    $results = mySQLNonQuery( $query );

    echo $results;
}

// --- LED Colour Change -----------------------------------------------------------
if(isset($_GET["colour"]))
{
    //error_log("LED Colour {$_GET["colour"]}");
    LEDColourDelete();
    LEDColourInsert($_GET["colour"]);
}

function LEDColourDelete()
{
    $query = "DELETE FROM LEDColour";

    $results = mySQLNonQuery( $query );

    // I can't echo here, it terminates the server process, equivalent to return in a function
    //echo $results;
}

function LEDColourInsert($value)
{
    $query = "INSERT INTO `LEDColour` (`HEX`) VALUES ('$value')";

    $results = mySQLNonQuery( $query );

    echo $results;
}


?>