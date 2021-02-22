
window.onload = Generuj_kometarze()

const glowne_pole = document.querySelector('.media-list')




const formater = new Intl.DateTimeFormat( 'pl', {
	day: 'numeric',
	month: 'long',
	year: 'numeric',
    hour: 'numeric',
    minute: 'numeric'

} );

function Generuj_kometarze(){
    

    fetch(`http://127.0.0.1:8000/api/Kometarze_Obrazka/${obrazek_id}/`)
    .then(response => response.json())
    .then(data => {
        
        if(!data.length){
            glowne_pole.innerHTML = '<div class=" h2 pl-5">Brak komentarzy</div>'
            return
        }
        console.log(data);
        
        data.forEach(kometarz => {
            console.log(kometarz);
            get_autor(kometarz.autor).then(data => {

                const pub_d = new Date(kometarz.data_publikacji)
                
                const data_publikacji = formater.format(pub_d)


                glowne_pole.innerHTML += `
                
                <li class="media">
                <a class="pull-left">
                    <img src="${data.img}"
                         width="100px" height="100px" alt="" class="rounded-circle">
                </a>
                <div class="media-body">
                    <span class="text-muted pull-right">
                        <a class="" href="{%url 'user-posts' ${komentarz.autor} %}"> <strong
                                class="text-primary">${data.username}</strong></a>
                    </span>
                    <small class="text-muted">${data_publikacji}</small>
                    <p class="ml-2">
                        ${kometarz.tresc}
                    </p>
                </div>
            </li>
            <p></p>
            `
                
            })

            

            
        });

    })
}

function get_autor(id){
    
    return fetch(`http://127.0.0.1:8000/api/user_profile/${id}/`)
    .then(response => response.json())
    .then(data => {
        return data
    })
    
}
const kom_pole = document.querySelector('.pole_kom')

document.querySelector('.dodaj_kom').addEventListener('click',()=>{

    dane = {
        tresc : kom_pole.value,
        obrazek : obrazek_id,
        autor : user_id
    }

    fetch(`http://127.0.0.1:8000/api/Kometarze_Obrazka/`,{
        method : 'POST',
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')
            },
        body: JSON.stringify(dane)
    }).then(()=>{


        kom_pole.value = ""
        glowne_pole.innerHTML = ""

        Generuj_kometarze()  
        document.querySelector('.toast-ikona').innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chat-right-text-fill" viewBox="0 0 16 16">
        <path d="M16 2a2 2 0 0 0-2-2H2a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h9.586a1 1 0 0 1 .707.293l2.853 2.853a.5.5 0 0 0 .854-.353V2zM3.5 3h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1 0-1zm0 2.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1 0-1zm0 2.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1z"/>
      </svg>`
        document.querySelector('.toast-body').innerText = 'Dodano komentarz'
    
        $('.toast').toast('show')
  
    })

})





