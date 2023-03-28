
// ensures document is loaded before contents are executed
$(document).ready(function(){

// Light Intensity Event Handler
$("#intensity").change(function()
{
    console.log("Desired intensity is " + this.value)
})

// Light Temperature Event Handler
$("#temperature").change(function()
{
    console.log("Desired temperature is " + this.value)
})

});






/*****************************
Function Name: AjaxRequest
Description: General purpose ajax call function
Parameters: 
    let ajaxOptions = {}; // empty ajax settings/config container
    ajaxOptions['url'] = url; // Where : assign server/service URL  *webservice.php
    ajaxOptions['type'] = 'GET'; // How : GET POST PUT DELETE PATCH
    ajaxOptions['data'] = sendData; // What do  you want to send ?
    ajaxOptions['dataType'] = 'html'; // html is default, text, json
    ajaxOptions['success'] = SuccessHandler; // DOOONOOTT Call it !! SuccessCallback() *TableMaker() is my success call here
    ajaxOptions['error'] = ErrorHandler;
$.ajax( ajaxOptions ); // Let 'er go !
Returns: Upon success calls associated function
****************************/
function AjaxRequest(url, type, data, dataType, successFunction, errorFunction){

    let ajaxFunctionData = {};
    ajaxFunctionData['url'] = url;
    ajaxFunctionData['type'] = type;
    ajaxFunctionData['data'] = data;
    ajaxFunctionData['dataType'] = dataType;
    ajaxFunctionData['success'] = successFunction; // DOOONOOTT Call it !! SuccessCallback()
    ajaxFunctionData['error'] = errorFunction; 

    $.ajax(ajaxFunctionData);
};