
window.onload = Generuj_kometarze()


const glowne_pole = document.querySelector('.media-list')

const formater = new Intl.DateTimeFormat( 'pl', {
	day: 'numeric',
	month: 'long',
	year: 'numeric',
    hour: 'numeric',
    minute: 'numeric'

} );



let list_snapshot = []
async function Generuj_kometarze(){
    
    const komentarze = await fetch(`http://127.0.0.1:8000/api/Kometarze_Obrazka/${obrazek_id}/`).then(response => response.json())

    if(!komentarze.length){
        glowne_pole.innerHTML = '<div class=" h2 pl-5">Brak komentarzy</div>'
        return
    }

    console.log(komentarze);

    const autorzy_id = []
    const autorzy = []

    komentarze.forEach(komentarz => {
        if(!autorzy_id.includes(komentarz.autor)){
            autorzy_id.push(komentarz.autor)
        }
    })

    console.log(autorzy_id);


    for(id of autorzy_id){
        const autor = await fetch(`http://127.0.0.1:8000/api/user_profile/${id}/`).then(r=> r.json())
        autorzy.push(autor)
    }



    for(let i in komentarze){
        
        try{
            document.querySelector(`#data-row-${i}`).remove()
        }catch(err){
        }

        const autor = autorzy.find(autor => autor.id == komentarze[i].autor)

        
        
        
         
        const data_publikacji = formater.format(new Date(komentarze[i].data_publikacji))

        
        const item = `<li id="data-row-${i}" class="media mb-2">
                                    <a class="pull-left">
                                        <img src="${autor.img}"
                                            width="100px" height="100px" alt="" class="rounded-circle">
                                    </a>
                                    <div class="media-body">
                                        <span class="text-muted pull-right">
                                            <a class="" href="/user/${autor.username}"> <strong
                                                    class="text-primary">${autor.username}</strong></a>
                                        </span>
                                        <small class="text-muted">${data_publikacji}</small>
                                        <p class="ml-2">
                                            ${komentarze[i].tresc}
                                        </p>
                                    </div>
                                </li> `

        glowne_pole.innerHTML += item

    }

    if(list_snapshot.length>komentarze.length){
        for(let i = komentarze.length; i< list_snapshot.length;i++){
            document.querySelector(`#data-row-${i}`).remove()
        }
    }

    list_snapshot = komentarze


    // komentarze.forEach(async kom => {
        
    //     console.log(kom);
    //     const autor = await fetch(`http://127.0.0.1:8000/api/user_profile/${kom.autor}/`).then(r=> r.json())

    //     console.log(autor);
    //     console.log('-------------------------------');
    //     glowne_pole.innerHTML+= `kom: ${kom.tresc} autor: <br>`
        

    // });


    
}





const kom_pole = document.querySelector('.pole_kom')

document.querySelector('.dodaj_kom').addEventListener('click',()=>{
    

    if(!kom_pole.value){
        document.querySelector('.toast-ikona').innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
      </svg>`
        document.querySelector('.toast-body').innerText = 'Nic nie wpisano'
    
        $('.toast').toast('show')
        return

    }

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
        // glowne_pole.innerHTML = ""
        

        Generuj_kometarze()  
        document.querySelector('.toast-ikona').innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chat-right-text-fill" viewBox="0 0 16 16">
        <path d="M16 2a2 2 0 0 0-2-2H2a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h9.586a1 1 0 0 1 .707.293l2.853 2.853a.5.5 0 0 0 .854-.353V2zM3.5 3h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1 0-1zm0 2.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1 0-1zm0 2.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1z"/>
      </svg>`
        document.querySelector('.toast-body').innerText = 'Dodano komentarz'
    
        $('.toast').toast('show')
  
    })

})





