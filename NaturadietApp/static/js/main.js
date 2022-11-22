window.addEventListener('load', iniciar, false);

function iniciar(){
    window.addEventListener('scroll', backTop, false);

    var images=['/static/img/background1.jpg',
                '/static/img/background2.jpg',
                '/static/img/background3.jpg',
                '/static/img/background4.jpg',
                '/static/img/background5.jpg',
                '/static/img/background6.jpg',];

    var numRandom = Math.floor(Math.random() * images.length);
    var bgImg = 'linear-gradient(rgba(71, 71, 71, 0.6), rgba(71, 71, 71, 0.6)), url(' + images[numRandom] + ')';

    var fondo = document.getElementById('fondo');

    fondo.style.backgroundImage = bgImg;
}



function backTop() {
    if(document.documentElement.scrollTop > 400){
        console.log(document.documentElement.scrollTop);
        document.getElementsByClassName('arriba')[0].style.display = 'block';
    }else{
        document.getElementsByClassName('arriba')[0].style.display = 'none';
    }
    
    document.getElementsByClassName('arriba')[0].addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}



