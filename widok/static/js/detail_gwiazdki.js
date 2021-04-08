const full_star = `<svg width="1em" height="1em" viewBox="0 0 16 16" class="mr-1 h1 bi bi-star-fill"
fill="currentColor" xmlns="http://www.w3.org/2000/svg">
<path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.283.95l-3.523 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
</svg>`
const half_star = `<svg width="1em" height="1em" viewBox="0 0 16 16" class="h1 mr-1 bi bi-star-half"
fill="currentColor" xmlns="http://www.w3.org/2000/svg">
<path fill-rule="evenodd"
    d="M5.354 5.119L7.538.792A.516.516 0 0 1 8 .5c.183 0 .366.097.465.292l2.184 4.327 4.898.696A.537.537 0 0 1 16 6.32a.55.55 0 0 1-.17.445l-3.523 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256a.519.519 0 0 1-.146.05c-.341.06-.668-.254-.6-.642l.83-4.73L.173 6.765a.55.55 0 0 1-.171-.403.59.59 0 0 1 .084-.302.513.513 0 0 1 .37-.245l4.898-.696zM8 12.027c.08 0 .16.018.232.056l3.686 1.894-.694-3.957a.564.564 0 0 1 .163-.505l2.906-2.77-4.052-.576a.525.525 0 0 1-.393-.288L8.002 2.223 8 2.226v9.8z"/>
</svg>`
const empty_star = `<svg width="1em" height="1em" viewBox="0 0 16 16" class="h1 mr-1 bi bi-star"
fill="currentColor" xmlns="http://www.w3.org/2000/svg">
<path fill-rule="evenodd"
    d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.523-3.356c.329-.314.158-.888-.283-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767l-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288l1.847-3.658 1.846 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.564.564 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"/>
</svg>`



const ocena_button = document.querySelector('.wyslij_ocene') || false

const podglad_gwiazdek = document.querySelector('.podglad_ocen')


if(ocena_button)ocena_button.addEventListener('click',dodaj_ocene)

function dodaj_ocene(){
  let nowa_ocena

  const radios = document.querySelectorAll("input[name='ocena']")
  radios.forEach(radio => ((radio.checked) ? nowa_ocena = radio.value : false))
 
  const dane = {
    ocena : nowa_ocena,
    
  }

  fetch(`/api/obrazek/${obrazek_id}/oceny/`,{
      method : 'POST',
      headers: {
          "Content-type": "application/json",
          "X-CSRFToken": getCookie('csrftoken')
          },
      body: JSON.stringify(dane)
  }).then(()=>{
    ocena_button.innerText = 'ocenione'

    ocena_button.disabled = true
    ocena_button.removeEventListener('click',dodaj_ocene)

    Generuj_podglad_gwiazdek()


    radios.forEach(a => a.disabled = true)

    document.querySelector('.toast-ikona').innerText = '⭐'
    document.querySelector('.toast-body').innerText = 'Dodano ocene '

    $('.toast').toast('show')

  })


}

function Generuj_podglad_gwiazdek(){

  fetch(`/api/obrazek/${obrazek_id}/oceny/`)
  .then(response => response.json())
  .then(oceny => {

    podglad_gwiazdek.innerHTML = ""
    
    let srednia = 0
    
    if(oceny.length)
        srednia = oceny.map(a=>a.ocena).reduce((a,v,i)=>(a*i+v)/(i+1))
    
    
   
    
    for(let i=0;i<Math.floor(srednia);i++){
      podglad_gwiazdek.innerHTML+=full_star
      
    }
    if(srednia%1){
      podglad_gwiazdek.innerHTML+=half_star
    }
    for(let i=0;i<5-Math.ceil(srednia);i++){
      podglad_gwiazdek.innerHTML+=empty_star
      
    }

    podglad_gwiazdek.innerHTML+=`<span class="font-weight-light  h4">${srednia.toFixed(1)}<small class='count_ocen text-muted'>${oceny.length} </small></span>`
    

  })

}

Generuj_podglad_gwiazdek()
