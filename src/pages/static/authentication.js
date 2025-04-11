
async function register(event) {
    const url = window.location.href + "/register"

    const formData = new FormData(event.target);
    console.log(formData)
    const username = formData.get('username')
    const password = formData.get('password')
    const result = formData.get("result")

    event.preventDefault();

    fetch(url,{
        method: 'POST',
        body: formData
    })
    .then(response =>{
        if (!response.ok){
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        result.value = response
        return response
    })
    .then(data =>{

        // Login
    })
    .catch(error => console.error('Error:', error));
}