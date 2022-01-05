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
