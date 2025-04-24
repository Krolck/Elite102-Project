
// Event listners for form submission
document.addEventListener("DOMContentLoaded", () =>{
    const registerForm = document.getElementById("register");
    const loginButton = document.getElementById("login")
    registerForm.addEventListener('submit', register)
    loginButton.addEventListener('click', function(){
    window.location.href = 'login'
    })
})



async function register(event) {

    
    const output = event.target.elements['output']
    
    const formData = new FormData(event.target)
    const data = Object.fromEntries(formData.entries())
    
    console.log(data)

    
    fetch("/register",{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })

    .then(response =>{

        console.log(response)
        // if there's an error, return the error message
        if (!response.ok){
            return response.json().then(errorData => {
                
                output.value = errorData.message 
                throw new Error(`HTTP Error: ${errorData.error}`);
                
            })
        }
        return response.json()
    })
    .then(data =>{
        // login if no errors
        output.value = data.message
        window.location.href = "/login"
    })
    .catch(error => {
        // return error
        console.error(error)
        
})
}

