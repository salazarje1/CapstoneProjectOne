const passwordUl = document.querySelector('#passwordUl');
const passwordInfo = document.querySelector('#passwordInfo');

passwordUl.addEventListener('click', async (e) => {
    if (e.target.id === 'passwordButton'){
        e.preventDefault()
        console.log(e.target.id)

        passwordInfo.innerHTML = ''; 

        const passwordId = e.target.dataset['password'];

        const div = e.target.parentElement.previousSibling.previousSibling;

        const res = await axios.get(`/passwords/${passwordId}/check`)
        console.log(res);

        if (res.status === 200){
            updateStatus('text-danger', div);

            const count = parseInt(res.data.data);
            passwordDetailsShow(count);
            

        } else if (res.status === 204){
            updateStatus('text-success', div);
            securePasswordDetailsShow();
        }
    }
})
