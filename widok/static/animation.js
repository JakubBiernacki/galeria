const menubaton = document.querySelector(".menu-btn")
const button = document.querySelector('.navbar-toggler')

let menuOpen = false

button.addEventListener('click',()=>{
    
    if(!menuOpen){
        menubaton.classList.add('open')
        menuOpen = true
    }
    else{
        menubaton.classList.remove('open')
        menuOpen = false
    }
    // (button.ariaExpanded === 'false')? menuOpen = false:menuOpen = true
})