function sendMes(toid) {
    if (toid == -1) return;
    toid2 = toid;
    var xhr = new XMLHttpRequest();
    var messa = document.getElementById('inputMessage').value;
    var body = 'token=' + encodeURIComponent(get_cookie('token')) + '&to=' + encodeURIComponent(toid) + '&mes=' + messa;
    xhr.open("POST", '/api/sendmessage', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function(){
        if(xhr.readyState == 4 && xhr.status == 200){
            location.reload();
        }
    }
    xhr.send(body);
}

function get_cookie ( cookie_name ){
    var results = document.cookie.match ( '(^|;) ?' + cookie_name + '=([^;]*)(;|$)' );
    if ( results )
        return ( unescape ( results[2] ) );
    return null;
}

let mesnowstr = document.getElementById('counterMes').textContent;
let strings = mesnowstr.split(' ')
let mesnowlocal = 0;
let mesnowglobal = 0;
let toid2 = -1;

if (strings[0] == 'Всего'){
    let timerId = setInterval(() => updateMessages(), 7000);
    mesnowlocal = parseInt(strings[1]);
    mesnowglobal = mesnowlocal;
}
else{

}

function updateMessages(){
    if (toid2 == -100) return;
    var requestAPI = new XMLHttpRequest();
    requestAPI.onreadystatechange = function(){
        if(requestAPI.readyState == 4 && requestAPI.status == 200){
            mesnowglobal = parseInt(requestAPI.responseText);
            if(mesnowglobal != mesnowlocal){
                location.reload();
            }
        }
    }
    url = '/api/getmessagesize?token=' + get_cookie('token') + '&toid=' + toid2.toString();
    requestAPI.open('GET', url)
    requestAPI.send();
}