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

