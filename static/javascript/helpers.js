// Email Helper Functions 

function appendSafeToPage(res){
    const h2 = document.createElement("h2");
    h2.classList.add('mt-5', 'mb-3'); 
    h2.innerText = 'This Email is Safe! No Breaches Found.';
    breachData.appendChild(h2);
}

function appendToPage(res){
    const h2 = document.createElement("h2");
    h2.classList.add('mt-5', 'mb-3'); 
    h2.innerText = 'Breach Data'; 
    breachData.appendChild(h2);
    res.data.forEach(breach => {
        const data = handleData(breach); 
        breachData.appendChild(data);
    });
}


function handleData(data) {
    const div = document.createElement('div');
    div.classList.add('card', 'mb-2'); 

    const cardDiv = document.createElement('div');
    cardDiv.classList.add('card-body');

    const h5 = document.createElement('h5');
    h5.classList.add('card-title');
    h5.innerHTML = data.Title;

    const h6 = document.createElement('h6');
    h6.classList.add('card-subtitle', 'mb-2', 'text-muted');
    h6.innerHTML = `Breached ${data.BreachDate}`;

    const p = document.createElement('p');
    p.classList.add('card-text');
    p.innerHTML = data.Description;

    cardDiv.append(h5, h6, p);
    div.appendChild(cardDiv);

    return div;
}

function updateEmailStatus(text, div){
    p = document.createElement('p');
    if(text === 'text-danger'){
        p.classList.add('text-danger');
        p.innerHTML = 'Breached'
    } else if(text === 'text-success'){
        p.classList.add('text-success');
        p.innerText = 'Safe'
    }
    div.innerHTML = '';
    div.appendChild(p);
}


// Password Helper functions

function securePasswordDetailsShow(){
    const h2 = document.createElement('h2');
    h2.innerText = "This Password Is Secure"

    passwordInfo.appendChild(h2);
}

function passwordDetailsShow(count){
    const h2 = document.createElement('h2');
    h2.innerText = 'Password Vulnerability';

    const passDiv = document.createElement('div');
    passDiv.classList.add('progress');

    const p = document.createElement('p');
    p.innerText = `Password has been breached ${count} times.`
    p.classList.add('text-muted');

    if(count <= 10){
        passDiv.innerHTML = '<div class="progress-bar bg-warning" role="progressbar" style="width: 10%" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"></div>'
    } else if (count <= 50) {
        passDiv.innerHTML = '<div class="progress-bar bg-warning" role="progressbar" style="width: 50%" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>'
    } else if (count <= 75) {
        passDiv.innerHTML = '<div class="progress-bar bg-warning" role="progressbar" style="width: 70%" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"></div>'
    } else if (count > 100) {
        passDiv.innerHTML = '<div class="progress-bar bg-danger" role="progressbar" style="width: 100%" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"></div>'
    } 

    passwordInfo.appendChild(h2);
    passwordInfo.appendChild(p);
    passwordInfo.appendChild(passDiv);
}

function updateStatus(text, div){
    p = document.createElement('p');
    if(text === 'text-danger'){
        p.classList.add('text-danger');
        p.innerHTML = 'Password is <strong>NOT</strong> secure'
    } else if(text === 'text-success'){
        p.classList.add('text-success');
        p.innerText = 'Password is secure'
    }
    div.innerHTML = '';
    div.appendChild(p);
}