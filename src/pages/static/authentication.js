



    // TODO:
    // Implement All authentication

document.addEventListener("DOMContentLoaded", () =>{
    const registerForm = document.getElementById("register");
    registerForm.addEventListener('submit', function(event){
    register(event, registerForm)
    })
})

async function register(event, registerForm) {

    
    const output = document.getElementById("output")
    const url = window.location.href + "/api/register"
    
    const formData = new FormData(event.target)
    const data = Object.fromEntries(formData.entries())
    
    console.log(data)

    
    fetch(url,{
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
        window.location.href = 'login'
    })
    .catch(error => {
        console.error(error)
        
})
}