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
function removeVideoFromPlaylist(){
    let videoId = $(this).parent().prev().attr("id");
    let playListId = $("aside > div > span[class='active']").attr("id");
    let csrftoken = getCookie('csrftoken');
    let data = {
        "playListId":playListId,
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
    fetch("/youtubeApp/remove_video_from_playlist/",options)
    .then(response => response.json())
    .then(info => {
        if(info.deleted){
            $("video[id="+videoId+"]").parent().remove();
        }
    })
    .catch(err => alert("something went wrong."));
}
function getVideosByPlayList(){
    $("aside > div > span:first-child").css("border-bottom","none")
    $("aside > div > span:first-child").removeClass("active");
    $(this).css("border-bottom","2px solid orange")
    $(this).addClass("active")
    let csrftoken = getCookie('csrftoken');
    let data = {
        "playListId":this.id
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
    fetch("/youtubeApp/get_videos_by_playlist/",options)
    .then(response => response.json())
    .then(info => {
        $(".playlists-grid-container").empty()
        $(".playlists-grid-container").append("<div></div>")
        if(info.hasOwnProperty("nothing")){
            let divElement = document.createElement("div")
            let h1Tag = document.createElement("h1")
            let textNode = document.createTextNode("Empty")
            h1Tag.appendChild(textNode)
            divElement.setAttribute("id","empty-videos")
            divElement.appendChild(h1Tag)
            divElement.setAttribute("class","jumbotron")
            $(".playlists-grid-container").append(divElement)
        }
        else{
            let videosContainer = document.createElement("div")
            videosContainer.setAttribute("class","videos-grid-container")
            let urls = info["urls"]
            let ids = info["ids"]
            let videoNames = info["videoNames"]
            let userNames = info["userNames"]
            let uploadedDates = info["uploadedDates"]

            for(let index=0;index<urls.length;index++){
                let id = ids[index]
                let url = urls[index]
                let videoName = videoNames[index]
                let userName = userNames[index]
                let uploadedDate = uploadedDates[index]
                let divElement = document.createElement("div")
                divElement.setAttribute("class","video")
                let videoElement = document.createElement("video")
                videoElement.setAttribute("id",id)
                videoElement.setAttribute("style","width:100%;height:170px;")
                let sourceElement = document.createElement("source")
                sourceElement.setAttribute("src",url)
                videoElement.appendChild(sourceElement)
                let boldElement = document.createElement("b")
                let textNode = document.createTextNode(videoName+" by "+userName)
                boldElement.appendChild(textNode)
                let textNode2 = document.createTextNode("Created: "+uploadedDate)
                divElement.appendChild(videoElement)
                let brElement = document.createElement("br")
                divElement.appendChild(brElement)
                let relativeContainer = document.createElement("div")
                relativeContainer.setAttribute("style","position:relative;")
                let absoluteContainer = document.createElement("div")
                let styles = "position:absolute;top:0px;right:20px;color:white;background-color:black;z-index:1;padding:2px 4px;border-radius:5px;display:none;"
                absoluteContainer.setAttribute("style",styles)
                absoluteContainer.innerHTML = "remove from playlist"
                let moreIcon = document.createElement("i")
                moreIcon.innerHTML = "more_vert"
                moreIcon.setAttribute("style","float:right;")
                moreIcon.setAttribute("class","material-icons")
                relativeContainer.appendChild(absoluteContainer)
                relativeContainer.appendChild(moreIcon)
                relativeContainer.appendChild(boldElement)
                relativeContainer.appendChild(brElement)
                relativeContainer.appendChild(textNode2)
                divElement.appendChild(relativeContainer)
                videosContainer.appendChild(divElement)
                $(moreIcon).on("click",function(){
                    $(this).prev().toggle();
                })
                $(absoluteContainer).on("click",removeVideoFromPlaylist)
            }
            $(".playlists-grid-container").append(videosContainer)
            addClickListeners()
        }
    })
    .catch(err => alert("something went wrong."));
}

function addClickListeners(){
    document.querySelectorAll(".videos-grid-container > .video > video").forEach(item => {
        item.addEventListener("click",function(){
            window.location = '/youtubeApp/play_video/'+this.id+'/';
        })
    })
}

document.querySelectorAll("aside > div > span:first-child").forEach(item => {
    item.addEventListener("click",getVideosByPlayList);
});

window.addEventListener("load",function(){
    $("aside > div > span:first-child").first().click()
});

function addPlayList(){
    let playListName = document.querySelector("#playlist-create-form input[type='text']").value;
    let csrftoken = getCookie('csrftoken');
    console.log(playListName);
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
            document.querySelector("#playlist-create-form input[type='text']").value = "";
            document.getElementById("playlist-error").style.display="none";
            let divEle = $("<div></div>")
            let spanEle = $("<span></span>").text(playListName)
            spanEle.attr("id",info["playListId"])
            divEle.append(spanEle)
            let removeEle = $("<div></div>").text("Remove playlist")
            divEle.append(removeEle)
            let moreIcon = $("<i></i>").text("more_vert")
            moreIcon.css("float","right")
            moreIcon.attr("class","material-icons")
            divEle.append(moreIcon)
            $("aside").append(divEle)
            spanEle.on("click",getVideosByPlayList)
            moreIcon.on("click",function(){
                $(this).prev().toggle();
            })
            removeEle.on("click",deletePlaylist);
        }
    })
    
}
function deletePlaylist(){
    let playlistId = $(this).prev().attr("id");
    let csrftoken = getCookie('csrftoken');
    let data = {
        "playListId":playlistId
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
    fetch("/youtubeApp/remove_playlist/",options)
    .then(response => response.json())
    .then(info => {
        if(info.deleted){
            window.location.reload();
        }
    })
    .catch(err => alert("something went wrong"));
}
$("aside > div > i").on("click",function(){
    $(this).prev().toggle();
})
$("aside > div > div").on("click",deletePlaylist);
