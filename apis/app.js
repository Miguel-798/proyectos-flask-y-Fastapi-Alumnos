//console.log('funcionando')

var formulario = document.getElementById('formulario');
var respuesta = document.getElementById('respuesta');

formulario.addEventListener('submit', async function(e){
    e.preventDefault();
    var datos = new FormData(formulario); 

    fetch('http://127.0.0.1:8000/login',{
        method:'POST',
        body: datos
    })     
    .then( Response => Response.json())
    .then( data => {
        console.log(data)
        if(data['detail'] === 'El usuario no es correcto'){
            respuesta.innerHTML =`
            <div class="alert alert-danger" role="alert">
                Llena todos los campos
            </div>
            `
        }else{
            respuesta.innerHTML =`
            <div class="alert alert-danger" role="alert">
                Bienvenido/a
            </div>
            `
        } 
    })
    
})
