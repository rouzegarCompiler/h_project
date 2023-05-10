const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const price = urlParams.get('price')
console.log(price);

let price_obj=document.getElementById("price")
console.log(price_obj)
price_obj.innerText=price.toString()+"دلار"