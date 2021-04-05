

if(!window.location.href.includes('obrazek')){
if( /Android|webOS|iPhone|iPad|Mac|Macintosh|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    document.querySelectorAll('.obr').forEach(el => el.classList.remove('obr'))
    document.querySelectorAll('.obr-bottom').forEach(el => el.classList.remove('obr-bottom'))

}
else{
const tl = gsap.timeline({defaults: {ease: 'power1.out'}});

tl.to('.obr',{y:'0%',duration:0.4,stagger:0.09})
tl.fromTo('.obr-bottom',{opacity:0},{opacity:1,duration:1},'-=0.5')
}
}
