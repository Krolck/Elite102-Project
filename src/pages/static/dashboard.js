// gets data from Jinja2 variable


let unregisterPressed = false

let unregisterButton = null

// button submissions
document.addEventListener("DOMContentLoaded", () => {
    unregisterButton = document.getElementById("unregister")
    const depositForm = document.getElementById("deposit");
    const withdrawForm =document.getElementById("withdraw");
    const usernameForm = document.getElementById("username");
    const passwordForm =document.getElementById("password");
    const transferForm = document.getElementById("transfer");
    depositForm.addEventListener('submit', deposit)
    withdrawForm.addEventListener('submit', withdraw)
    usernameForm.addEventListener('submit', changeUsername)
    passwordForm.addEventListener('submit', changePassword)
    transferForm.addEventListener('submit', transfer)




})


async function deposit(event) {

    const welcomeText = document.getElementById('welcome')
    const output = event.target.elements['output']
    
    const formData = new FormData(event.target)
    // get input data to upload to the server
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

        // update the result and welcome text
        const history = document.getElementById("history")
        const item = document.createElement("li")
        item.textContent = data.history
        history.prepend(item)
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
        const history = document.getElementById("history")
        const item = document.createElement("li")
        item.textContent = data.history
        history.prepend(item)
        output.value = data.message
        welcomeText.textContent = `You have currently have $${data.balance} in your balance.`
    })
    .catch(error => {
        console.error(error)
        
})
}

async function transfer(event) {
    const welcomeText = document.getElementById('welcome')
    const output = event.target.elements['output']
    
    const formData = new FormData(event.target)
    const data = Object.fromEntries(formData.entries())

    fetch("transfer",{
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
        const history = document.getElementById("history")
        const item = document.createElement("li")
        item.textContent = data.history
        history.prepend(item)
        output.value = data.message
        welcomeText.textContent = `You have currently have $${data.balance} in your balance.`
    })
    .catch(error => {
        console.error(error)
        
})
}

async function logout() {
    fetch("logout",{
        method: 'GET',
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
        const history = document.getElementById("history")
        const item = document.createElement("li")
        item.textContent = data.history
        history.prepend(item)
        output.value = data.message
        welcomeHeader.textContent =  `Hello ${inputData['value']}!`
    })
    .catch(error => {
        console.error(error)
        
})
}


async function changePassword(event) {

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
        const history = document.getElementById("history")
        const item = document.createElement("li")
        item.textContent = data.history
        history.prepend(item)
        output.value = data.message
    })
    .catch(error => {
        console.error(error)
        
})
}

