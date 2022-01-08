
function upload(event) {
    var data = new FormData($('#profile-change-form').get(0));
    const options = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
        },
        mode: 'same-origin',
        body: data
    }
    fetch($(this).attr("action"),options)
    .then(response => response.json())
    .then(info => {
        if(info.changed){
            let url = info["url"];
            $("#profile").attr("src",url);
            $("#profile").click();
        }
    })
    .catch(err => alert("something went wrong."));

    return false;
}
$("#profile-change-form").submit(upload);

function check(){
    alert($('input[type=file]').val());
}

$("input[name='profile']").change(function(){
    $("#profile-change-form").submit();
});

$("#change-profile-link").click(function(event){
    $("input[name='profile']").click();
    return false;
})



