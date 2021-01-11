const back = document.querySelector('#back')
    back.addEventListener('click',(e)=>{
        let link = localStorage.getItem("poprzednia") || "/";
        window.location.href = link;
    })