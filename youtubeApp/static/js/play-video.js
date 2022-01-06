document.getElementById("profile").addEventListener("click",function(event){
    let ele = document.getElementById("user-options");
    if(ele.style.display == "block"){
        ele.style.display = "none";
    }
    else{
        ele.style.display = "block";
    }
});
document.querySelector('.upload-video span').addEventListener("click",function(){
    window.location = "/youtubeApp/upload_video/"
});
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function like(user,videoId){
    if(user == "None"){
        alert("sign in");
    }
    else {
        let csrftoken = getCookie('csrftoken');
        let data = {
            "username": user,
            "videoId": videoId
        }
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrftoken
            },
            mode: 'same-origin',
            body: JSON.stringify(data)
        }
        fetch("/youtubeApp/like/",options)
        .then(response => response.json())
        .then(info => {
            let likeClassList = document.querySelector('.like span').classList;
            let dislikeClassList = document.querySelector('.dislike span').classList;
            if(info.created){
                likeClassList.remove("fa-thumbs-o-up");
                likeClassList.add("fa-thumbs-up");
            }
            else{
                likeClassList.remove("fa-thumbs-up");
                likeClassList.add("fa-thumbs-o-up");
            }
            dislikeClassList.remove("fa-thumbs-down");
            dislikeClassList.add("fa-thumbs-o-down");
        });
    }
}

function dislike(user,videoId){
    if(user == "None"){
        alert("sign in");
    }
    else {
        let csrftoken = getCookie('csrftoken');
        let data = {
            "username": user,
            "videoId": videoId
        }
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrftoken
            },
            mode: 'same-origin',
            body: JSON.stringify(data)
        }
        fetch("/youtubeApp/dislike/",options)
        .then(response => response.json())
        .then(info => {
            let likeClassList = document.querySelector('.like span').classList;
            let dislikeClassList = document.querySelector('.dislike span').classList;
            if(info.created){
                dislikeClassList.remove("fa-thumbs-o-down");
                dislikeClassList.add("fa-thumbs-down");
            }
            else{
                dislikeClassList.remove("fa-thumbs-down");
                dislikeClassList.add("fa-thumbs-o-down");
            }
            likeClassList.remove("fa-thumbs-up");
            likeClassList.add("fa-thumbs-o-up");
        });
    }
}

function generateUrl(){
    navigator.clipboard.writeText(window.location.href);
    let ele = document.getElementById("share-tooltip");
    ele.style.display = "block";
    setTimeout(function(){
        ele.style.display = "none";
    },2000);
}

function saveVideo(event,user,videoId){
    event.preventDefault();
    if(user == "None"){
        alert("Sign In");
        document.getElementsByClassName("modal")[0].removeAttribute("id");
    }
    else{
        let csrftoken = getCookie('csrftoken');
        let data = {
            "username":document.body.id,
            "videoId":videoId
        }
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrftoken
            },
            mode: 'same-origin',
            body: JSON.stringify(data)
        }
        fetch("/youtubeApp/get_playlists/",options)
        .then(response => response.json())
        .then(info => {
            document.getElementById("playlist-error").style.display="none";
            document.querySelector(".playlist-form input[type='text']").value = "";
            document.querySelector(".playlist-form").style.display = "none";
            document.getElementById("create-playlist-btn").style.display = "block";
            
            let playlists = info["data"];
            let modalBodyElement = document.querySelector("#myModal .modal-body");
            modalBodyElement.innerHTML = '';
            for(let playlist of playlists){
                let divElement = document.createElement("div");
                divElement.setAttribute("class","checkbox");
                let labelElement = document.createElement("label");
                let inputElement = document.createElement("input");
                inputElement.setAttribute("type","checkbox");
                inputElement.setAttribute("value",playlist["id"]);
                if(playlist["checked"]){
                    inputElement.setAttribute("checked",true);
                }
                let textNode = document.createTextNode(playlist["name"]);
                labelElement.appendChild(inputElement);
                labelElement.appendChild(textNode);
                divElement.appendChild(labelElement);
                modalBodyElement.appendChild(divElement);
            }
            addCheckboxListeners();
        });
    }
}
function addClickListener(event){
    let username = document.body.id;
    let videoId = document.getElementsByClassName("video-to-watch")[0].id;
    let playListId = this.value;
    let csrftoken = getCookie('csrftoken');
    let checked = this.checked;
    let data = {
        "username": username,
        "videoId": videoId,
        "playListId":playListId,
        "checked":checked
    }
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken
        },
        mode: 'same-origin',
        body: JSON.stringify(data)
    }
    fetch("/youtubeApp/add_to_playlist/",options)
    .then(response => response.json())
    .then(info => {
        if(info.success){
            console.log("Modified.");
        }
    })
    .catch(err => alert("Permission Denied."));
}
function addCheckboxListeners(){
    document.querySelectorAll('.checkbox input[type="checkbox"]').forEach(item => {
        item.addEventListener("click",addClickListener);
    });
}

function showPlayListForm(){
    document.getElementById("create-playlist-btn").style.display="none";
    document.querySelector(".playlist-form").style.display="block";
}
function addPlayList(){
    let playListName = document.querySelector(".playlist-form input[type='text']").value;
    let csrftoken = getCookie('csrftoken');
    let data = {
        "username":document.body.id,
        "playListName":playListName
    }
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken
        },
        mode: 'same-origin',
        body: JSON.stringify(data)
    }
    fetch("/youtubeApp/create_new_playlist/",options)
    .then(response => response.json())
    .then(info => {
        if(info.hasOwnProperty("existed")){
            document.getElementById("playlist-error").style.display="block";
        }
        else{
            document.getElementById("playlist-error").style.display="none";
            document.querySelector(".playlist-form input[type='text']").value = "";
            document.querySelector(".playlist-form").style.display = "none";
            document.getElementById("create-playlist-btn").style.display = "block";
            let modalBodyElement = document.querySelector("#myModal .modal-body");
            let divElement = document.createElement("div");
            divElement.setAttribute("class","checkbox");
            let labelElement = document.createElement("label");
            let inputElement = document.createElement("input");
            inputElement.setAttribute("type","checkbox");
            inputElement.setAttribute("value",info["playListId"]);
            inputElement.addEventListener("click",addClickListener);
            let textNode = document.createTextNode(playListName);
            labelElement.appendChild(inputElement);
            labelElement.appendChild(textNode);
            divElement.appendChild(labelElement);
            modalBodyElement.appendChild(divElement);
        }
    })
    .catch(err => alert("Permission Denied"));
}
