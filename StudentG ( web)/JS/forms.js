const url = "http://127.0.0.1:8000"
serverBusy = false


function showLogin() {
    document.getElementById('loginForm').classList.add('active-form');
    document.getElementById('signupForm').classList.remove('active-form');
    document.getElementById('loginBtn').classList.add('active');
    document.getElementById('signupBtn').classList.remove('active');
}

function showSignup() {
    document.getElementById('signupForm').classList.add('active-form');
    document.getElementById('loginForm').classList.remove('active-form');
    document.getElementById('signupBtn').classList.add('active');
    document.getElementById('loginBtn').classList.remove('active');
}

async function handleLogin() {
    if(serverBusy) return
    let url_login = `${url}/account/login`;
    serverBusy = true

    data = {
        username : $("Username-L").value,
        password: $("Password-L").value,
    }

    try{
        var response = await fetch(url_login,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
            credentials: "include"
        })

        var res = await response.json()

        if(!res.loggedin){
            const div = document.createElement("div")
            div.className = "notif";
            div.textContent = `🔔 ${res.message}`
            document.body.appendChild(div)
            await wait(1000)
            div.remove()
            serverBusy = false
        }else{
            window.location.href="dashboard.html"
        }

    }catch(e){
        const div = document.createElement("div")
        div.className = "notif";
        div.textContent = `Error - No Internet Or Server Down `
        document.body.appendChild(div)
        await wait(1000)
        div.remove()
        serverBusy = false
    }
}

async function handleSignup() {
    if(serverBusy) return
    let url_signup = `${url}/account/signup`;
    serverBusy = true

    data = {
        username : $("username-S").value,
        password: $("password-S").value,
        confirmPassword: $("Confirmpassword-S").value,
        email: $("email-S").value
    }

    try{
        var response = await fetch(url_signup, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
            credentials: "include"
        })

        var res = await response.json()
        console.log(res.loggedin)
        
        if(!res.loggedin){
            const div = document.createElement("div")
            div.className = "notif";
            div.textContent = `🔔 ${res.message}`
            document.body.appendChild(div)
            await wait(1000)
            div.remove()
            serverBusy = false
        }else{
            window.location.href="dashboard.html"
        }
    }catch(e){
        const div = document.createElement("div")
        div.className = "notif";
        div.textContent = `Error - No Internet Or Server Down`
        document.body.appendChild(div)
        await wait(1000)
        div.remove()
        serverBusy = false
    }
}