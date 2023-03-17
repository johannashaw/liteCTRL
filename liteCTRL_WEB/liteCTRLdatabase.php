<?php

$connection = null;
$response = "";

Connect();

function Connect()
{
    global $connection, $response;

    $connection = new mysqli("localhost", "litectrl", "cmpe_012345678", "litectrl_Test");

    if ($connection->connect_error)
    {
        $response = "Connect Error (" .$connection->connect_errno . ") " . $connection->connect_error;
        error_log($response);
        die();
    }
    else
    {
        error_log("Connection Successfully Established");
    }
        
}

function mySQLQuery( $query )
{
    global $connection, $response;

    $result = false;
    
    if ($connection == null)
    {
        $response = "No database connection established";
        return $result;
    }

    if (!($result = $connection->query($query)))
    {
        
        $response = "Query Error : {$connection->errno} : {$connection->error}";
    }
    error_log(json_encode( $connection));
    
    return $result;

}

function mySQLNonQuery( $query )
{
    global $connection, $response;

    $result = -1;

    if ($connection == null)
    {
        $response = "No database connection established";
        return $result;
    }

    if (!($result = $connection->query($query)))
    {
        
        $response = "Query Error : {$connection->errno} : {$connection->error}";
        return $result;
    }

    return $connection->affected_rows;

}

