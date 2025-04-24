document.addEventListener("DOMContentLoaded", () =>{
    const loginForm = document.getElementById("login");
    const registerbutton = document.getElementById("register");
    loginForm.addEventListener('submit', login)
    registerbutton.addEventListener('click', function(){
        window.location.href = '/' 

    })
})

async function login(event) {
    
    const output = event.target.elements['output']
    const formData = new FormData(event.target)
    const data = Object.fromEntries(formData.entries())
    

    
    fetch("login",{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })

    .then(response =>{       
        if (!response.ok){
            return response.json().then(errorData => {
                // error
                output.value = errorData.message 
                throw new Error(`HTTP Error: ${errorData.error}`);
                
            })
        }
        return response.json()
    })
    .then(data =>{
        // success
        output.value = data.message
        window.location.href = "/dashboard"
    })
    .catch(error => {
        // return error
        console.error(error)
        
})
}

