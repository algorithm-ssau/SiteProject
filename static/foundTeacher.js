function foundTeacher() {
    var requestAPI = new XMLHttpRequest();
    let resultWithTeachers;
    var request = new XMLHttpRequest();
    let prefab;
    let result = '';
    let url = '/api/found/teacher/?city=';
    requestAPI.onreadystatechange = function(){
        if(requestAPI.readyState == 4 && requestAPI.status == 200){
            resultWithTeachers = JSON.parse(requestAPI.responseText);
            if(resultWithTeachers.length == 0){
                search_result_id_block.innerHTML = 'Репетиторы, подходящие под фильтр, не найдены('
            }
            else{
                request.open('GET', '/prefabs/teacher');
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

    let expmin = document.getElementById("experienceMin").value;
    if (expmin != '')
        url += '&expmin=' + expmin;

    let expmax = document.getElementById("experienceMax").value;
    if (expmax != '')
        url += '&expmax=' + expmax;

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

    let ratemin = document.getElementById("rateMin").value;
    if (ratemin != '')
        url += '&ratemin=' + ratemin;

    let ratemax = document.getElementById("rateMax").value;
    if (ratemax != '')
        url += '&ratemax=' + ratemax;

    let EduS = document.getElementById("edus")
    if (EduS.checked)
        url += '&edstudent=1';

    let EduA = document.getElementById("edua")
    if (EduA.checked)
        url += '&edaspir=1';

    let EduT = document.getElementById("edut")
    if (EduT.checked)
        url += '&edteacher=1';

    let EduP = document.getElementById("edup")
    if (EduP.checked)
        url += '&edprepod=1';

    let sex=document.getElementsByName('sex');
    if (sex[1].checked) url += '&sex=m';
    if (sex[2].checked) url += '&sex=w';

    requestAPI.open('GET', url)
    requestAPI.send();

    
    request.onreadystatechange = function(){
        if(request.readyState == 4 && request.status == 200){
            prefab = request.responseText;
            resultWithTeachers.forEach(teacher => addTeacher(teacher));
            search_result_id_block.innerHTML = result;
        }
    }

    function addTeacher(teacher){
        newPrefab = prefab.substring(0);
        newPrefab = newPrefab.replace('{{URL}}', '/user/' + teacher['ID']);
        newPrefab = newPrefab.replace('{{LASTNAME}}', teacher['Фамилия']);
        newPrefab = newPrefab.replace('{{FIRSTNAME}}', teacher['Имя']);
        newPrefab = newPrefab.replace('{{EDUCATION}}', teacher['Образование']);
        newPrefab = newPrefab.replace('{{EXP}}', teacher['Стаж_преподавания_в_годах'].toString());
        newPrefab = newPrefab.replace('{{RATE}}', teacher['Ставка_в_час'].toString());
        if(teacher['Фотография'] == 'Стандарт'){
            newPrefab = newPrefab.replace('{{PHOTO}}', 'https://api.adorable.io/avatars/234/' + teacher['ID'].toString());
        }
        else{
            newPrefab = newPrefab.replace('{{PHOTO}}', "/images/" + teacher['ID'].toString() + ".png");
        }
        
        result += newPrefab;
    }

}