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

$(".video > div > i").click(function(){
    $(this).prev().toggle();
});
$(".video > video").click(function(){
    window.location = '/youtubeApp/play_video/'+$(this).attr("id")+'/';
})
$(".video > div > div").click(function(){
    let videoId = $(this).parent().prev().prev().attr("id");
    let csrftoken = getCookie('csrftoken');
    let data = {
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
    fetch("/youtubeApp/delete_video/",options)
    .then(response => response.json())
    .then(info => {
        if(info.deleted){
            $("video[id="+videoId+"]").parent().remove();
        }
    })
    .catch(err => alert("somethig went wrong."));
})
