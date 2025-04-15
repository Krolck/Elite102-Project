
    // TODO:
    // Implement All authentication
document.addEventListener("DOMContentLoaded", () =>{
    const registerForm = document.getElementById("register");
    const loginButton = document.getElementById("login")
    registerForm.addEventListener('submit', register)
    loginButton.addEventListener('click', function(){
    window.location.href = 'login'
    })
})



async function register(event) {

    
    const output = document.getElementById("output")
    
    const formData = new FormData(event.target)
    const data = Object.fromEntries(formData.entries())
    
    console.log(data)

    
    fetch("/api/register",{
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
                output.value = errorData.message 
                throw new Error(`HTTP Error: ${errorData.error}`);
                
            })
        }
        return response.json()
    })
    .then(data =>{
        output.value = data.message
        window.location.href = "login"
    })
    .catch(error => {
        console.error(error)
        
})
}

