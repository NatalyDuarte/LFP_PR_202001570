function Evaluar(){
    alert("entrada");
    let area= document.getElementById("area1")
    area.removeAttribute("hidden")
}
function Evaluar1(){
    alert("info")
    let area1= document.getElementById("area2")
    let texto= document.getElementById("texto")
    let select1 = document.querySelector("select").value
    //let radio = document.querySelector("input[name=\"inlineRadioOptions\"]:checked").value
    //alert(radio)
        document.getElementById("area2").innerText =texto.value
        document.getElementById("area2").innerText =select1
        document.getElementById("area2").innerText =texto.value + "  "+select1
    
    //document.getElementById("area2").innerText = radio
    //document.getElementById("area2").innerText =texto.value + "  "+select1
    //document.getElementById("txarea2").innerText = select1
    area1.removeAttribute("hidden");

}