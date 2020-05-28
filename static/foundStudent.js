function foundStudent() {
    var requestAPI = new XMLHttpRequest();
    let resultWithTeachers;
    var request = new XMLHttpRequest();
    let prefab;
    let result = '';
    let counter = 1;
    let url = '/api/found/student/?city=';
    requestAPI.onreadystatechange = function(){
        if(requestAPI.readyState == 4 && requestAPI.status == 200){
            resultWithTeachers = JSON.parse(requestAPI.responseText);
            if(resultWithTeachers.length == 0){
                search_result_id_block.innerHTML = 'Ученики, подходящие под фильтр, не найдены('
            }
            else{
                request.open('GET', '/prefabs/student');
                request.send();
            }
        }
    }

    function get_cookie ( cookie_name ){
        var results = document.cookie.match ( '(^|;) ?' + cookie_name + '=([^;]*)(;|$)' );
        if ( results )
            return ( unescape ( results[2] ) );
        return null;
    }

    search_result_id_block.innerHTML = 'Загружаем...';
    window.scrollTo(0, 0);

    url += get_cookie('citycode');

    let ttos = document.getElementById("a1checkid")
    if (ttos.checked)
        url += '&ttos=1';
    
    let stot = document.getElementById("a2checkid")
    if (stot.checked)
        url += '&stot=1';

    let distance = document.getElementById("a3checkid")
    if (distance.checked)
        url += '&distance=1';

    let Less1 = document.getElementById("Less1")
    if (Less1.checked)
        url += '&math=1';

    let Less2 = document.getElementById("Less2")
    if (Less2.checked)
        url += '&rus=1';

    let Less3 = document.getElementById("Less3")
    if (Less3.checked)
        url += '&phys=1';

    let Less4 = document.getElementById("Less4")
    if (Less4.checked)
        url += '&inf=1';

    let Less5 = document.getElementById("Less5")
    if (Less5.checked)
        url += '&chemistry=1';

    let Less6 = document.getElementById("Less6")
    if (Less6.checked)
        url += '&bio=1';

    let Less7 = document.getElementById("Less7")
    if (Less7.checked)
        url += '&history=1';

    let Less8 = document.getElementById("Less8")
    if (Less8.checked)
        url += '&social=1';
    
    let Less9 = document.getElementById("Less9")
    if (Less9.checked)
        url += '&literature=1';

    let Less10 = document.getElementById("Less10")
    if (Less10.checked)
        url += '&geo=1';

    let Less11 = document.getElementById("Less11")
    if (Less11.checked)
        url += '&economy=1';

    let Less12 = document.getElementById("Less12")
    if (Less12.checked)
        url += '&eng=1';

    let Less13 = document.getElementById("Less13")
    if (Less13.checked)
        url += '&dutch=1';

    let classmin = document.getElementById("classMin").value;
        url += '&classmin=' + classmin;

    let classmax = document.getElementById("classMax").value;
        url += '&classmax=' + classmax;

    let sex=document.getElementsByName('sex');
    if (sex[1].checked) url += '&sex=m';
    if (sex[2].checked) url += '&sex=w';

    requestAPI.open('GET', url)
    requestAPI.send();

    
    request.onreadystatechange = function(){
        if(request.readyState == 4 && request.status == 200){
            prefab = request.responseText;
            resultWithTeachers.forEach(student => addStudent(student));
            search_result_id_block.innerHTML = result;
        }
    }

    function addStudent(student){
        newPrefab = prefab.substring(0);
        newPrefab = newPrefab.replace('{{NUMBER}}', counter.toString());
        counter++;
        newPrefab = newPrefab.replace('{{LASTNAME}}', student['Фамилия']);
        newPrefab = newPrefab.replace('{{FIRSTNAME}}', student['Имя']);
        newPrefab = newPrefab.replace('{{CLASS}}', student['Класс']);
        if(student['Фотография'] == 'Стандарт'){
            newPrefab = newPrefab.replace('{{PHOTO}}', 'https://api.adorable.io/avatars/234/' + student['ID'].toString());
        }
        else{
            newPrefab = newPrefab.replace('{{PHOTO}}', "/images/" + student['ID'].toString() + ".png");
        }
        
        result += newPrefab;
    }

}