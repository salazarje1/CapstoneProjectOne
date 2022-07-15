const form = document.querySelector('#form');
const simpleEmailCheck = document.querySelector('#simpleEmailCheck');

form.addEventListener('submit', async (e) => {
    e.preventDefault(); 

    simpleEmailCheck.innerHTML = ''; 
    
    const email = document.querySelector('input').value;

    const res = await axios.get(`/simple-check/${email}`)

    if(res.status === 200){
        simpleDisplayInfo(email, true);
    } else if (res.status === 204){
        simpleDisplayInfo(email, false);
    }
})


function simpleDisplayInfo(email, breached){
    const h5 = document.createElement('h6');
    h5.classList.add('text-muted', 'mt-3')
    if(breached){
        h5.innerHTML = `${email.toUpperCase()} has been breached. For more information <a href="/login">login</a>.`;
    } else {
        h5.innerHTML = `${email.toUpperCase()} has not been breached.`
    }
    simpleEmailCheck.appendChild(h5);
}