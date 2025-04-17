const balance = "{{balance}}"

let unregisterPressed = false

let unregisterButton = null

document.addEventListener("DOMContentLoaded", () => {
    unregisterButton = document.getElementById("unregister")
    const depositForm = document.getElementById("deposit");
    const withdrawForm =document.getElementById("withdraw");
    const usernameForm = document.getElementById("username");
    const passwordForm =document.getElementById("password");
    depositForm.addEventListener('submit', deposit)
    withdrawForm.addEventListener('submit', withdraw)
    usernameForm.addEventListener('submit', changeUsername)
    passwordForm.addEventListener('submit', changePassword)
    
})


async function deposit(event) {

    const welcomeText = document.getElementById('welcome')
    const output = event.target.elements['output']
    
    const formData = new FormData(event.target)
    const data = Object.fromEntries(formData.entries())

        

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
                output.value = errorData.message 
                throw new Error(`HTTP Error: ${errorData.error}`);
                
            })
        }
        return response.json()
    })
    .then(data =>{
        output.value = data.message
        welcomeText.textContent = `You have currently have $${data.balance} in your balance.`
    })
    .catch(error => {
        console.error(error)
        
})
}

async function withdraw(event) {

    const welcomeText = document.getElementById('welcome')
    const output = event.target.elements['output']
    
    const formData = new FormData(event.target)
    const data = Object.fromEntries(formData.entries())

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
                output.value = errorData.message 
                throw new Error(`HTTP Error: ${errorData.error}`);
                
            })
        }
        return response.json()
    })
    .then(data =>{
        output.value = data.message
        welcomeText.textContent = `You have currently have $${data.balance} in your balance.`
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


async function unregister() {
    if (!unregisterPressed){
        unregisterPressed = true
        unregisterButton.textContent = "Are you sure?"
        return
    }

    fetch("unregister",{
        method: 'POST',
        headers: {
        },
    })
    window.location.href = "/login"
        
}
async function changeUsername(event) {

    const welcomeHeader = document.getElementById('welcomeHeader')
    const output = event.target.elements['output']
    const formData = new FormData(event.target)
    const inputData = Object.fromEntries(formData.entries())

        

    fetch("username",{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputData)
    })

    .then(response =>{       
        if (!response.ok){
            return response.json().then(errorData => {
                output.value = errorData.message 
                throw new Error(`HTTP Error: ${errorData.error}`);
                
            })
        }
        return response.json()
    })
    .then(data =>{
        
        output.value = data.message
        welcomeHeader.textContent =  `Hello ${inputData['value']}!`
    })
    .catch(error => {
        console.error(error)
        
})
}


async function changePassword(event) {

    const welcomeHeader = document.getElementById('welcomeHeader')
    const output = event.target.elements['output']
    const formData = new FormData(event.target)
    const inputData = Object.fromEntries(formData.entries())

        

    fetch("password",{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputData)
    })

    .then(response =>{       
        if (!response.ok){
            return response.json().then(errorData => {
                output.value = errorData.message 
                throw new Error(`HTTP Error: ${errorData.error}`);
                
            })
        }
        return response.json()
    })
    .then(data =>{
        output.value = data.message
    })
    .catch(error => {
        console.error(error)
        
})
}