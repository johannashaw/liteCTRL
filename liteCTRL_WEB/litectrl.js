automaticModeFlag = null

// ensures document is loaded before contents are executed
$(document).ready(function(){

// Populate webpage inputs with previously saved values from database
GetSettingsAjax()


// Sweet sweet sunrise
ColourWash()

// Light Intensity Event Handler
$("#intensity").change(function()
{
    number = Number(this.value)
    if (0 <= number & number <= 100 )
    {
        console.log("Desired intensity is " + this.value)
        $("#intensity").css("background-color", "white")
        LightIntensityAjax(this.value)
    }
    else{
        $("#intensity").css("background-color", "red")
        $("#intensity").val("No")
    }
    
})

// Light Temperature Event Handler
$("#temperature").change(function()
{
    number = Number(this.value)
    if (0 <= number & number <= 100 )
    {
        console.log("Desired temperature is " + this.value)
        $("#temperature").css("background-color", "white")
        LightTemperatureAjax(this.value)
    }
    else{
        $("#temperature").css("background-color", "red")
        $("#temperature").val("No")
    }

    
})

// Curtain Position Event Handler
$("#curtain").change(function()
{
    console.log("Curtain position is " + this.value)
    CurtainPositionAjax(this.value)
})

// LED Colour Event Handler
$("#colour").change(function()
{
    console.log("LED colour is " + this.value)
    LEDColourAjax(this.value)
})

// event handlers to specify automatic or manual selection

$("#automaticMenu").click(function(){
    console.log("automatic menu click")
    if(!automaticModeFlag)
    {
        AutomaticMode()
        SystemModeAjax("automatic")
        automaticModeFlag = true
    }
})

$("#manualMenu").click(function(){
    console.log("manual menu click")
    if(automaticModeFlag)
    {
        ManualMode()
        SystemModeAjax("manual")
        automaticModeFlag = false
    }
})

}); // --- End of ready function block -------------------------------------------------------

function AutomaticMode(){
    $("#manualMenu > div").css("color", "gray")
    $("#curtain").prop("disabled", true)
    $("#colour").prop("disabled", true)

    $("#automaticMenu > div").css("color", "white")
    $("#intensity").prop("disabled", false)
    $("#temperature").prop("disabled", false)
}

function ManualMode(){
    $("#automaticMenu > div").css("color", "gray")
    $("#intensity").prop("disabled", true)
    $("#temperature").prop("disabled", true)

    $("#manualMenu > div").css("color", "white")
    $("#curtain").prop("disabled", false)
    $("#colour").prop("disabled", false)
}

// --- function to handle colouring of page -----------------------------------------------
function ColourWash()
{
    
    
    setTimeout(function(){
        State1()
        setTimeout(function(){
            State2()
            setTimeout(function(){
                State3()
                setTimeout(function(){
                    State4()
                    setTimeout(function(){
                        State5()
                        setTimeout(function(){
                            State6()
                            setTimeout(function(){
                                State7()
                                setTimeout(function(){
                                    State8()
                                }, 50)
                            }, 75)
                        }, 100)
                    }, 500) // Pause on full colour
                }, 300)
            }, 250)
        }, 200)
    }, 200)
    
}

// --- Sunrise States ---------------------------------------------------------------------

function State1(){
    $("footer").attr("class", "calico")
}

function State2(){
    $("footer").attr("class", "poloblue")
    $("#manualMenu").attr("class", "calico")
}

function State3(){
    $("footer").attr("class", "towergray")
    $("#manualMenu").attr("class", "poloblue")
    $("#automaticMenu").attr("class", "calico")
}

function State4(){
    $("footer").attr("class", "abbey")
    $("#manualMenu").attr("class", "towergray")
    $("#automaticMenu").attr("class", "poloblue")
    $("#header").attr("class", "calico")
}

// --- Sunset States ---------------------------------------------------------------------- 

function State5(){
    $("footer").attr("class", "towergray")
    $("#manualMenu").attr("class", "poloblue")
    $("#automaticMenu").attr("class", "calico")
    $("#header").attr("class", "")
}

function State6(){
    $("footer").attr("class", "poloblue")
    $("#manualMenu").attr("class", "calico")
    $("#automaticMenu").attr("class", "")
}

function State7(){
    $("footer").attr("class", "calico")
    $("#manualMenu").attr("class", "")
}

function State8(){
    $("footer").attr("class", "")
}

// --- ajax call to retrieve all settings values from database ----------------------------
function GetSettingsAjax(){
    console.log("In get settings ajax")
    let sendData = {}
    sendData["settings"] = "hello :)";

    return AjaxRequest("webservice.php", "GET", sendData, "json", GetSettingsSuccess, GetSettingsAjaxError)
}
function GetSettingsSuccess(data)
{
    console.log("Get Settings Success")
    console.log(data)

    $("#intensity").val(data["LightIntensity"]["Value"])
    $("#temperature").val(data["LightTemperature"]["Value"])
    $("#curtain").val(data["CurtainPosition"]["Value"])
    $("#colour").val(data["LEDColour"]["HEX"])

    if(data["SystemMode"]["Mode"] == "automatic")
    {
        AutomaticMode()
        automaticModeFlag = true
    }
    else
    {
        ManualMode()
        automaticModeFlag = false
    }

    

}
function GetSettingsAjaxError()
{
    console.log("Get Settings Ajax Error")
}


// --- ajax call to set system mode ------------------------------------------------------

function SystemModeAjax(systemMode){
    console.log("In system mode ajax")
    let sendData = {}
    sendData["systemmode"] = systemMode;

    AjaxRequest("webservice.php", "GET", sendData, "json", SystemModeSuccess, SystemModeAjaxError)
}
function SystemModeSuccess()
{
    console.log("System Mode Success")
}
function SystemModeAjaxError()
{
    console.log("System Mode Ajax Error")
}
// --- ajax call to save changed input value to database ----------------------------------

function LightIntensityAjax(intensityValue){
    console.log("In light intensity change ajax")
    let sendData = {}
    sendData["intensity"] = intensityValue;

    AjaxRequest("webservice.php", "GET", sendData, "json", LightIntensitySuccess, LightIntensityAjaxError)
}
function LightIntensitySuccess()
{
    console.log("Light Intensity Success")
}
function LightIntensityAjaxError()
{
    console.log("Light Intensity Ajax Error")
}

// -------------------------------------------------------------------------------------------

function LightTemperatureAjax(temperatureValue){
    console.log("In light temperature change ajax")
    let sendData = {}
    sendData["temperature"] = temperatureValue;

    AjaxRequest("webservice.php", "GET", sendData, "json", LightTemperatureSuccess, LightTemperatureAjaxError)
}
function LightTemperatureSuccess()
{
    console.log("Light Temperature Success")
}
function LightTemperatureAjaxError()
{
    console.log("Light Temperature Ajax Error")
}

// -------------------------------------------------------------------------------------------

function CurtainPositionAjax(curtainValue){
    console.log("In curtain position change ajax")
    let sendData = {}
    sendData["curtain"] = curtainValue;

    AjaxRequest("webservice.php", "GET", sendData, "json", CurtainPositionSuccess, CurtainPositionAjaxError)
}
function CurtainPositionSuccess()
{
    console.log("Curtain Position Success")
}
function CurtainPositionAjaxError()
{
    console.log("Curtain Position Ajax Error")
}

// -------------------------------------------------------------------------------------------

function LEDColourAjax(colourValue){
    console.log("In LED colour change ajax")
    let sendData = {}
    sendData["colour"] = colourValue;

    AjaxRequest("webservice.php", "GET", sendData, "json", LEDColourSuccess, LEDColourAjaxError)
}
function LEDColourSuccess()
{
    console.log("LED Colour Success")
}
function LEDColourAjaxError()
{
    console.log("LED Colour Ajax Error")
}




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