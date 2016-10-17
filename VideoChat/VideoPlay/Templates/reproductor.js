function init(){
    maximo=600;
    video=document.getElementById('video');
    reproducir=document.getElementById('reproducir');
    bar=document.getElementById('bar');
    progress=document.getElementById('progress');

    reproducir.addEventListener('click',push,false);
    bar.addEventListener('click',move,false);
}

//Permite que la barra de progreso vaya aumentando de acuerdo a la canción
function estado(){
    if(!video.ended){
        var total = parseInt(video.currentTime*maximo/video.duration);
        progress.style.width=total+'px';
    } else {
        progress.style.width='0px';
        reproducir.innerHTML='Play';
        window.clearInterval(loop);
    }
}

//Adelantar o retrasar el video
function move(e){
    if(!video.paused &&!video.ended){
        var ratonX=e.pageX-bar.offsetLeft;
        var nuevoTiempo=ratonX*video.duration/maximo;
        video.currentTime=nuevoTiempo;
        progress.style.width=ratonX+'px';
    }
}

window.addEventListener('load',init,false);

