
    // TODO:
    // Implement All authentication
document.addEventListener("DOMContentLoaded", () =>{
    const loginForm = document.getElementById("login");
    const registerbutton = document.getElementById("register");
    loginForm.addEventListener('submit', login)
    registerbutton.addEventListener('click', function(){
        window.location.href = '/' 
        // CHANGE ROUTE LATER
    })
})

async function login(event) {

    
    const output = document.getElementById("output")
    
    const formData = new FormData(event.target)
    const data = Object.fromEntries(formData.entries())
    
    console.log(data)

    
    fetch("/api/login",{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })

    .then(response =>{

        console.log(response)
        if (!response.ok){
            return response.json().then(errorData => {
                // REMEMBER to change errors to change depending on code rather than relying on server
                output.value = errorData.error 
                throw new Error(`HTTP Error: ${errorData.error}`);
                
            })
        }
        return response.json()
    })
    .then(data =>{
        output.value = data.message
        window.location.href = '/dashboard'
    })
    .catch(error => {
        console.error(error)
        
})
}

