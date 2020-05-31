function save(){
    let elements = document.querySelectorAll('textarea');
    message = ''
    for (let elem of elements) {
      message+='&'+elem.id.toString()+'='+encodeURIComponent(elem.value);
    }
    url = 'token=' + encodeURIComponent(get_cookie('token')) + message;
    

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/api/savenotes', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function(){
        if(xhr.readyState == 4 && xhr.status == 200){
            location.reload();
        }
    }
    xhr.send(url);
}

function get_cookie ( cookie_name ){
    var results = document.cookie.match ( '(^|;) ?' + cookie_name + '=([^;]*)(;|$)' );
    if ( results )
        return ( unescape ( results[2] ) );
    return null;
}