function get_cookie ( cookie_name ){
    var results = document.cookie.match ( '(^|;) ?' + cookie_name + '=([^;]*)(;|$)' );
    if ( results )
        return ( unescape ( results[2] ) );
    return null;
}

function newNode() {
    let url = '/api/newnote?token=' + get_cookie('token');
    var requestAPI = new XMLHttpRequest();
    var request = new XMLHttpRequest();
    let noteID;
    requestAPI.onreadystatechange = function(){
        if(requestAPI.readyState == 4 && requestAPI.status == 200){
            noteID = requestAPI.responseText;
            request.open('GET', '/prefabs/timetable');
            request.send();
        }
    }
    request.onreadystatechange = function(){
        if(request.readyState == 4 && request.status == 200){
            prefab = request.responseText;
            prefab = prefab.replace('{{DATEID}}', noteID);
            prefab = prefab.replace('{{DATE}}', '');
            prefab = prefab.replace('{{TASK}}', '');
            prefab = prefab.replace('{{LESSONID}}', noteID);

            let elements = document.querySelectorAll('textarea');
            messages = []
            for (let elem of elements) {
                messages.push(elem.value);
            }

            var count = messages.length;
            tasklist.innerHTML += prefab;
            messages = messages.reverse();

            elements = document.querySelectorAll('textarea');
            var index = 0;
            for (let elem of elements) {
                if(index < count){
                    elem.value = messages.pop();
                    index++;
                }
                
            }
        }
    }
    requestAPI.open('GET', url);
    requestAPI.send();
}