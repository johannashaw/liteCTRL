<?php

require_once "liteCTRLdatabase.php";

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

?>