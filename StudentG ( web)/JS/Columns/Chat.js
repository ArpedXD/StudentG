// -------- CHAT FUNCTIONALITY ------ [COLUMN : CHAT - dont remove so it'll be easy to find each dashboard section]
$("create-chat").addEventListener("click", ()=>{
    $("create-group-modal").classList.toggle("active")
    $("blurryBG").classList.toggle("active")
})

$("create-group-no").addEventListener("click", ()=>{
    $("create-group-modal").classList.toggle("active")
    $("blurryBG").classList.toggle("active")
})

$("group-settings-exit").addEventListener("click", ()=>{
    $("group-modal").style.display = "none"
    $("blurryBG").classList.remove("active")
})

// group-settings modal
var group_settings_list = ["invite_modal", "group-list-modal"] // for the UI of the button

let activeBTN = null;

document.querySelectorAll(".group-setting-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        if(activeBTN == btn.dataset.target){
            return
        }
        
        group_settings_list.forEach(id => {
            $(id).classList.add("deactivate");
        });

        $(btn.dataset.target).classList.remove("deactivate");

        activeBTN = btn.dataset.target

        if(btn.dataset.target == "group-list-modal") showMembers()
    });
});


// --- bluepint to create new groups
//<div id="Group" class="Group">
//    <><div class="group-pic"></div><div id="group-name" class="group-name">The underdogs</div></>
// </div>

group_code = {

}

async function createGroupChat(){
    var url_createGroup = `${url}/chat/create`

    data = {
        group_name: $("group_name").value
    }

    var response = await fetch(url_createGroup, {
        method: "POST",
        headers: {
            'Content-type': 'Application/json'
        },
        body: JSON.stringify(data),
        credentials: "include"
    })

    var res = await response.json()
    console.log(res.Reason)
    $("create-group-modal").classList.toggle("active")
    $("blurryBG").classList.toggle("active")
}

var spamPrevention;
async function GroupLoad(){
    loadedMessage=0
    history.pushState({}, "", `dashboard.html?chat=`)

    let Gload_url = `${url}/chat/Groupload`

    var response = await fetch(Gload_url,{
        method: "GET",
        credentials: "include"
    })

    if(!response.ok){
        console.log("er")
        throw new Error("Something went wrong!");
    }

    $("chatlist").querySelectorAll(".Group").forEach(el => el.remove())
    for(const item of await response.json()){
        group_code[item[0]] = item[1]
        let div = document.createElement("div")
        div.id = "Group"
        div.className = "Group"
        div.innerHTML = `<div class="group-pic"></div><div id="group-name" class="group-name">${item[0]}</div>`
        div.addEventListener("click", ()=>{
            $("chat_layout").classList.add("active")
            if(spamPrevention == item[1]) return;
            spamPrevention = item[1]
            createDivGroups(item[1])
            load_messages()
        })
        $("chatlist").appendChild(div)
    }

    console.log(group_code)
}

async function createDivGroups(item){
    socket.close()
    history.pushState({}, "", `dashboard.html?chat=${item}`)
    const params = new URLSearchParams(window.location.search);
    socket = new WebSocket(`ws://127.0.0.1:8000/chat/connect?chat=${item}`)
    socket.addEventListener('message', (event) =>{
        console.log("res")
        response = JSON.parse(event.data)
        OtherUser = document.createElement("div")
        OtherUser2 = document.createElement("div")
        OtherUser2.innerHTML = renderMarkdown(response.message)
        OtherUser2.setAttribute("data-secret-id", response.id)
        OtherUser.className = "other-message";
        OtherUser2.className = "other-message msg";
        OtherUser.textContent = response.username;
        $("chat-messages").appendChild(OtherUser)
        $("chat-messages").appendChild(OtherUser2);
        $("chat-messages").scrollTop = $("chat-messages").scrollHeight;
    })
}

let sentAmessage = false
async function sendMessage(){
    if (sentAmessage) {
        return raiseError(new ErrorTypes().SendingTooQuickly)
    }
    newDiv = document.createElement("div")
    newDiv2 = document.createElement("div")
    newDiv.className = "user-message"
    newDiv.textContent = "You"
    newDiv2.textContent = $("chatbox").value
    $("chat-messages").appendChild(newDiv)
    newDiv.appendChild(newDiv2)
    $("chat-messages").scrollTop = $("chat-messages").scrollHeight
    sentAmessage = true
    socket.send($("chatbox").value)

    if($("chatbox").value == "/req"){
        let res = await fetch('http://localhost:5678/webhook-test/aef31b59-e5e4-45f2-ab1e-abee09f33b9b', {
            method:'GET',
            headers:{
                'mynigga' : 'myultimatenigga',
            }
        })


    }
    $("chatbox").value = ""
    await wait(1000)
    sentAmessage = false
}

let loadedMessage = 10;
async function load_messages(){
    $("chat-messages").innerHTML = ""
    var Qparameter = new URLSearchParams(window.location.search);
    var Qparameter = Qparameter.get("chat")
    let url_message = `${url}/chat/load_messages?chat=${Qparameter}&messages=10`

    response = await fetch(url_message, {
        method: "GET",
        credentials: "include",
    })
    await load_message_response(await response)
    $("chat-messages").scrollTop = $("chat-messages").scrollHeight
}

var last_id = null
async function load_message_response(response){
    for(const each of await response.json()){
        if(each.username == "Me"){
            newDiv = document.createElement("div")
            newDiv2 = document.createElement("div")
            newDiv.className = "user-message"
            newDiv.textContent = "You"
            newDiv2.textContent = each.message
            $("chat-messages").prepend(newDiv)
            newDiv.prepend(newDiv2)
        }else{
            OtherUser = document.createElement("div")
            OtherUser2 = document.createElement("div")
            OtherUser2.textContent = each.message
            OtherUser.className = "other-message";
            OtherUser2.className = "other-message msg";
            OtherUser.textContent = each.username;
            $("chat-messages").prepend(OtherUser2);
            $("chat-messages").prepend(OtherUser)
        }
        last_id = each.id
    }
}

$("chat-messages").addEventListener("scroll", async (e)=>{
    if($("chat-messages").scrollTop == 0) {
        var Qparameter = new URLSearchParams(window.location.search);
        var Qparameter = Qparameter.get("chat")
        let url_message = `${url}/chat/load_messages?chat=${Qparameter}&messages=10&before=${last_id}`
        let response = await fetch(url_message, {
            method:'GET',
            credentials: "include",
        })

        if(response.ok){
            await load_message_response(response)
        }
    }
})

$("search_user").addEventListener("input", update)

async function update(){
    $("group-user-list").innerHTML = ""
    if ($("search_user").value == "" || $("search_user").value.replace(/\s/g, "") == "") return
    url_search = `${url}/chat/search_user`
    data = $("search_user").value

    request = await fetch(url_search,{
        method: "POST",
        headers:{
            "Content-type": "text/plain"
        },
        body: data
    })

    res = await request.json()
    savedId = res
    for(const each in res){
        let users = document.createElement("div")
        let circ_username = document.createElement("div")
        let username = document.createElement("div")

        users.className = "users"
        circ_username.className = "circ-username"
        username.className = "username"

        username.textContent = res[each][0]
        $("group-user-list").append(users)
        users.append(circ_username)
        users.append(username)
        
        // sets attribute to secret idea
        users.setAttribute("data-secret-id", res[each][1])
        circ_username.setAttribute("data-secret-id", res[each][1])
        username.setAttribute("data-secret-id", res[each][1])

        users.addEventListener("click", (event)=>{
            const secret = event.target.dataset.secretId;
            console.log(secret)
        })

        users.addEventListener("contextmenu",(e)=>{
            e.preventDefault()
            $("custom-menu-invite").style.left = `${event.pageX}px`;
            $("custom-menu-invite").style.top = `${event.pageY}px`;
            $("custom-menu-invite").style.display = "block";
            TargetID = e.target.dataset.secretId
        })
    }
}

async function showMembers(){   
    $("group-list-modal").innerHTML = ""
    var Qparameter = new URLSearchParams(window.location.search);
    var Qparameter = Qparameter.get("chat")
    let url_showmembers = `${url}/chat/showMembers?chat=${Qparameter}`

    let response = await fetch(url_showmembers, {
        method: 'GET',
        credentials: 'include'
    })
    
    if(!response.ok){
        throw new Error("Something went Wrong!")
    }

    res = await response.json()
    console.log(res)
    for(const each in res){
        let users = document.createElement("div")
        let circ_username = document.createElement("div")
        let username = document.createElement("div")

        users.className = "users"
        circ_username.className = "circ-username"
        username.className = "username"

        username.textContent = res[each][0]
        $("group-list-modal").append(users)
        users.append(circ_username)
        users.append(username)

        users.setAttribute("data-secret-id", res[each][1])
        circ_username.setAttribute("data-secret-id", res[each][1])
        username.setAttribute("data-secret-id", res[each][1])

        users.addEventListener("contextmenu",(e)=>{
            e.preventDefault()
            $("custom-menu-show").style.left = `${event.pageX}px`;
            $("custom-menu-show").style.top = `${event.pageY}px`;
            $("custom-menu-show").style.display = "block";
            TargetID = e.target.dataset.secretId
            console.log(TargetID)
        })
    }
}

$("chat-menu").addEventListener("click", async ()=>{
    var Qparameter = new URLSearchParams(window.location.search);
    var Qparameter = Qparameter.get("chat")
    let isAdmin_url = `${url}/chat/isAdmin?chat=${Qparameter}`

    let response = await fetch(isAdmin_url, {
        method: 'GET',
        credentials: 'include'
    })

    if(await response.json()){
        $("group-modal").style.display = "flex"
        $("blurryBG").classList.add("active")
    }else{
        raiseError(new ErrorTypes().NoAdminAccess)
    }
})

async function InviteUser(ID){
    var Qparameter = new URLSearchParams(window.location.search);
    var Qparameter = Qparameter.get("chat")
    let Invite_url = `${url}/chat/invite?chat=${Qparameter}&target_user=${ID}`

    let request = await fetch(Invite_url, {
        method: 'GET',
        credentials: 'include'
    })

    if(!request.ok){
        raiseError(new ErrorTypes().UserAlreadyHere)
    }
}

async function RemoveUser(ID){
    var Qparameter = new URLSearchParams(window.location.search);
    var Qparameter = Qparameter.get("chat")
    let remove_url = `${url}/chat/remove?chat=${Qparameter}&target_user=${ID}`

    let request = await fetch(remove_url, {
        method: 'GET',
        credentials: 'include'
    })

    if(!request.ok){
        raiseError(new ErrorTypes().UserAlreadyHere)
    } else{
        showMembers()
    }
}