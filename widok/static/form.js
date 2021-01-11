
const link = document.querySelector("input[name='obrazek_path']");
const podglad = document.querySelector("#podglad");



link.addEventListener('focusout', (event)=>{

    document.querySelector('.rounded').remove();
    let nowy = document.createElement('img');
    nowy.classList = 'rounded';
    nowy.src = event.target.value;
    if( !nowy.onerror && nowy.src.match(/\.(jpeg|jpg|gif|png)$/) != null)
    {
        nowy.height=200;
        
    }
    else{
        alert("Link jest nie poprawny");
        nowy.src = "https://static.thenounproject.com/png/558475-200.png";
    }
    podglad.appendChild(nowy)


})