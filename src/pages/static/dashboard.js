const balance = "{{balance}}"

document.addEventListener("DOMContentLoaded", () => {

    const depositForm = document.getElementById("deposit");
    const withdrawForm =document.getElementById("withdraw");
    depositForm.addEventListener('submit', deposit)
    withdrawForm.addEventListener('submit', withdraw)
})

async function deposit(event) {

    const balanceText = document.getElementById('balance')
    const output = event.target.elements['output']
    
    const formData = new FormData(event.target)
    const data = Object.fromEntries(formData.entries())
    // if (data['amount'] > "{{ balance }}"){
    //     output.value = "Not Enough Money"
    // }
        

    fetch("deposit",{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })

    .then(response =>{       
        if (!response.ok){
            return response.json().then(errorData => {
                // REMEMBER to change errors to change depending on code rather than relying on server
                output.value = errorData.message 
                throw new Error(`HTTP Error: ${errorData.error}`);
                
            })
        }
        return response.json()
    })
    .then(data =>{
        output.value = data.message
        balanceText.textContent = `You have currently have $${data.balance} in your balance.`
    })
    .catch(error => {
        console.error(error)
        
})
}

async function withdraw(event) {

    const balanceText = document.getElementById('balance')
    const output = event.target.elements['output']
    
    const formData = new FormData(event.target)
    const data = Object.fromEntries(formData.entries())
    if (data['amount'] > "{{ balance }}"){
        output.value = "Not Enough Money"
    }
        

    fetch("withdraw",{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })

    .then(response =>{       
        if (!response.ok){
            return response.json().then(errorData => {
                // REMEMBER to change errors to change depending on code rather than relying on server
                output.value = errorData.message 
                throw new Error(`HTTP Error: ${errorData.error}`);
                
            })
        }
        return response.json()
    })
    .then(data =>{
        output.value = data.message
        balanceText.textContent = `You have currently have $${data.balance} in your balance.`
    })
    .catch(error => {
        console.error(error)
        
})
}


async function logout() {
    fetch("logout",{
        method: 'POST',
        headers: {
        },
    })
    window.location.href = "/login"
        
}