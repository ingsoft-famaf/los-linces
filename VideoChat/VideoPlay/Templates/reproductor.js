function iniciar(){
    maximo=600;
    medio=document.getElementById('medio');
    reproducir=document.getElementById('reproducir');
    barra=document.getElementById('barra');
    progreso=document.getElementById('progreso');

    reproducir.addEventListener('click',presionar,false);
    barra.addEventListener('click',mover,false);
}

function presionar(){
    if(!medio.paused && !medio.ended){
        medio.pause();
        reproducir.innerHTML='Play';
        window.clearInterval(bucle);
    } else {
        medio.play();
        reproducir.innerHTML= 'Pause';
        bucle= setInterval(estado, 1000);
    }
}

//Permite que la barra de progreso vaya aumentando de acuerdo a la canción
function estado(){
    if(!medio.ended){
        var total = parseInt(medio.currentTime*maximo/medio.duration);
        progreso.style.width=total+'px';
    } else {
        profreso.style.width='0px';
        reproducir.innerHTML='Play';
        window.clearInterval(bucle);
    }
}

//Adelantar o retrasar el videp
function mover(e){
    if(!medio.paused &&!medio.ended){
        var ratonX=e.pageX-barra.offsetLeft;
        var nuevoTiempo=ratonX*medio.duration/maximo;
        medio.currentTime=nuevoTiempo;
        progreso.style.width=ratonX+'px';
    }
}

window.addEventListener('load',iniciar,false);

