const emailUl = document.querySelector('#emailUl');
const mainDiv = document.querySelector('#main');
const breachData = document.querySelector('#breachData');


emailUl.addEventListener('click', async (e) => {
    if(e.target.id === 'emailButton'){
        e.preventDefault();

        breachData.innerHTML = ''; 

        const emailId = e.target.dataset['email'];

        const res = await axios.get(`/emails/${emailId}/check`)

        if(res.status === 200){
            appendToPage(res);
        } else if (res.status === 204){
            appendSafeToPage(res)
        }

    }
})


