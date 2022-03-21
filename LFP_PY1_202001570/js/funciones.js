function Evaluar(){
    alert("entrada")
    let area= document.getElementById("area1")
    area.removeAttribute("hidden")
}
function Evaluar1(){
    alert("info")
    let area1= document.getElementById("area2")
    let texto= document.getElementById("texto")
    document.getElementById("area2").innerText =texto.value
    area1.removeAttribute("hidden")
    
}