const formatter = new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP',
    minimumFractionDigits: 0
  })
  


let urlIndicadores = "https://mindicador.cl/api";

fetch(urlIndicadores)
.then(function(respuesta){
    return respuesta.json();
})
.then(function(respuesta){
    let valorUf = document.getElementById("valorUF");
    
    valorUf.innerHTML =  formatter.format(Math.round(respuesta.uf.valor));

    let valorDolar = document.getElementById("valorDolar");

    valorDolar.innerHTML= formatter.format(Math.round(respuesta.dolar.valor));

    let valorEuro = document.getElementById("valorEuro");

    valorEuro.innerHTML = formatter.format(Math.round(respuesta.euro.valor));

    let valorUtm = document.getElementById("valorUTM");

    valorUtm.innerHTML =  formatter.format(Math.round(respuesta.utm.valor));

    let valorBitcoin = document.getElementById("valorBitcoin");

    valorBitcoin.innerHTML =  formatter.format(Math.round(respuesta.bitcoin.valor));


})