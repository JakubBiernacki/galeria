const tl = gsap.timeline({defaults: {ease: 'power1.out'}});

tl.to('.obr',{y:'0%',duration:0.4,stagger:0.09})
tl.fromTo('.obr-bottom',{opacity:0},{opacity:1,duration:1},'-=0.5')


