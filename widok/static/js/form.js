
const spin = document.getElementById('spin')
const newspin = {spin}


//file podglad
function readURL(input) {

  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#blah').attr('src', e.target.result);
    }

    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}

$("#id_obrazek_file").change(function() {
  readURL(this);
  spin.remove();
});


const link = document.querySelector("input[name='obrazek_path']");
const podglad = document.querySelector("#podglad");

link.addEventListener('focusout', (event)=>{
    let poprzedni = document.getElementsByClassName('rounded')[0];
    console.log(Boolean(poprzedni));

    (poprzedni)?poprzedni.remove():false;
    // document.querySelector('.rounded').remove();
    let nowy = document.createElement('img');
    nowy.classList = 'rounded';
    nowy.src = event.target.value;
    if( !nowy.onerror && nowy.src.match(/\.(jpeg|jpg|gif|png)$/) != null && nowy.src.startsWith('https://') )
    {
        nowy.height=200;
        podglad.appendChild(nowy);
        spin.remove()
    }
    else{

        podglad.appendChild(spin);

    }
})






