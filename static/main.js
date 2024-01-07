
const userForm = document.querySelector("#userForm");

let users = [];
let editing = false;
let userId = null;

//
window.addEventListener("DOMContentLoaded", async () => {
  // users = await fetch("/api/users");
  // const data = await users.json();
  users = await fetch("/api/users").then((response) => response.json());

  if(users){
  renderUsers(users);
  };

});


//
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

   if(!editing) {
     const response = await fetch("/api/users", {
       method: "POST",
       headers: {
         "Content-Type": "application/json",
       },
       body: JSON.stringify({
         username,
         email,
         password,
       }),
     });

     const data = await response.json();

     users.unshift(data);
   } else {

    const response = await fetch(`/api/users/${userId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        email,
        password,
      }),
    });

    const updatedUser = await response.json();

    users = users.map((user) => user.id === updatedUser.id ? updatedUser : user);
    editing = false;
    userId = null;
   };

    renderUsers(users);

    userForm.reset();
    
});


//
function renderUsers(users) {

  const userList = document.querySelector('#userList');

  userList.innerHTML = '';

  users.forEach(user => {
    const userItem = document.createElement('li');

    userItem.classList = 'list-group-item list-group-item-dark my-2'
    userItem.innerHTML = `
     <header class="d-flex justify-content-between align-items-center">
      <h3>${user.username}</h3>
      <div>
       <button class="btn-delete btn btn-danger btn-sm">delete</button>
       <button class="btn-edit btn btn-secondary btn-sm">edit</button>
      </div>
     </header>
     <p>${user.email}</p>
     <p class="text-truncate">${user.password}</p>
    `;

    const btnDelete = userItem.querySelector('.btn-delete');

    btnDelete.addEventListener('click', async () => {
       const response = await fetch(`/api/users/${user.id}`, {
        method: "DELETE"
       });

       const data = await response.json();

       users = users.filter(user => user.id !== data.id);

       renderUsers(users);

    });
//
    const btnEdit = userItem.querySelector(".btn-edit");

    btnEdit.addEventListener('click', async () => {
      const response = await fetch(`/api/users/${user.id}`);
      const data = await response.json();
      console.log(data);

      userForm["username"].value = data.username;
      userForm["email"].value = data.email;
      userForm["password"].value = data.password;

      editing = true;
      userId = data.id;

    });

    


    userList.appendChild(userItem);
   });
  

};


