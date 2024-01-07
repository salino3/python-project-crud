
const userForm = document.querySelector("#userForm");

userForm.addEventListener('submit', async event => {
    event.preventDefault();
    
    //* It doen't work
    // const username = userForm["username"];
    // const email = userForm["email"];
    // const password = userForm["password"];
    // console.log(username.value, email.value, password.value);
    

    const formData = new FormData(userForm);

    const username = formData.get("username");
    const email = formData.get("email");
    const password = formData.get("password");

    const response = await fetch("/api/users", {
      method: "POST",
      headers: {
        'Content-Type': "application/json",
      },
      body: JSON.stringify({
        username,
        email,
        password,
      }),
    });

    const data = await response.json();

    console.log("data->", data);
    userForm.reset();
    
});



