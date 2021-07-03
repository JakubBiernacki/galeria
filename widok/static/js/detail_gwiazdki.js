const full_star = `<i class="fas fa-star"></i>`
const half_star = `<i class="fas fa-star-half-alt"></i>`
const empty_star = `<i class="far fa-star"></i>`



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
