const url = "http://127.0.0.1:8000"
var socket;
let TargetID = null; //FOR CONTEXT MENu

// Easily Accessible Error using : new ErrorTypes().ERRORTYPE
class ErrorTypes{
    constructor(){
        this.NoAdminAccess = "NOT AUTHORIZED"
        this.UserAlreadyHere = "USER IS ALREADY HERE"
        this.SendingTooQuickly = "You're sending a message too QUICKLY."
    }
}

navList = [
    "HomeD",
    "ChatD", 
    "AnnouncementD", 
    "AssignmentD", 
    "AutomatedD", 
    "NotificationD"
]

navParams = [
    "home",
    "chat",
    "announcement",
    "assignment",
    "automated",
    "notification"
]
WebStartHandler()
async function WebStartHandler(){

    const params = new URLSearchParams(window.location.search);
    const param = Object.fromEntries(params);
    id = Object.keys(param)[0]
    for(i = 0; i < navParams.length;i++){
        if(id == navParams[i]) {
            nav(navList[i])
        }
    }
    let url_loggedin = `${url}/chat/isLoggedin`
    
    res = await fetch(url_loggedin,{
        method: "get",
        credentials: "include"
    })

    if(!res.ok){
        throw new Error("Not Logged In!");
    }

    socket = new WebSocket(`ws://127.0.0.1:8000/chat/connect?chat=`)
}

async function nav(id){
    if(id != "ChatD") $("chat_layout").classList.remove("active") // -- ensures that chat layout wont be removed when left navigation bar is not removed --
    if($(id).classList.contains("active")) return
    if(id == "ChatD") await GroupLoad()
    if(id == "HomeD") await HomeLoad()

    $(id).classList.add("active")
    navList.forEach(element => {
        if(element == id) return $(id).classList.add("active")
        return $(element).classList.remove("active")
    });
}
// ----------- HOME FUNCTIONALITY [COLUMN : HOME]
async function HomeLoad() {
    history.pushState({}, "", `dashboard.html?home=`)
}


document.addEventListener("click", () => { // USED FOR CLICKING THE DOCUMENT ITSELF TO DO A FUNCTION [EX: Removing the Custom ContextMenu]
    console.log("running")
    // <--- Context Menu
    $("custom-menu-show").style.display = "none"; // Removes Context Menu
    $("custom-menu-invite").style.display = "none";
    TargetID = null // Removes ID of the context Menu
})


// context-menu
async function menuAction(Action){
    if(Action == "Invite") InviteUser(TargetID)
    if(Action == "Remove") RemoveUser(TargetID)
}


async function raiseError(errorCode){
    $("custom-error").style.display = "flex"
    $("Error-code").innerHTML = errorCode
    await wait(2000)
     $("custom-error").style.display = "none"
}

function renderMarkdown(markdown) {
    if (typeof marked !== 'undefined') {
        // marked v5+ uses marked.parse(), older versions use marked()
        if (typeof marked.parse === 'function') {
            return marked.parse(markdown);
        }
        return marked(markdown);
    }
    return markdown;
}