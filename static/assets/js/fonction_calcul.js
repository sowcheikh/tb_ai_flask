function FormatEncodage(chaine){
    return chaine
            .replaceAll("&#39;","'")
            .replaceAll("&#34;","\"")
            .replaceAll("&amp;", "&")
            .replaceAll("&lt;","<")
            .replaceAll("&gt;",">")
            .replaceAll("<br>","\n")
    
}
function getDay(){
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; 
    var yyyy = today.getFullYear();

    if(dd<10){
        dd='0'+dd;
    } 
    if(mm<10){
        mm='0'+mm;
    } 
    today = yyyy+'-'+mm+'-'+dd;
    return today
}

function getWeekNumber(d) {
    // Copy date so don't modify original
    d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    // Set to nearest Thursday: current date + 4 - current day number
    d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay()||7));
    // Get first day of year
    var yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1));
    // Calculate full weeks to nearest Thursday
    var weekNo = Math.ceil((((d - yearStart) / 86400000) + 1)/7);
    if (weekNo.toString().length==1){
        return  d.getFullYear().toString() +'-W0'+weekNo.toString();
    }
    else{
        return  d.getFullYear().toString() +'-W'+weekNo.toString();
    }
}

function getWeekNumberPreced(d) {
    // Copy date so don't modify original
    d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()-7));
    // Set to nearest Thursday: current date + 4 - current day number
    d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay()||7));
    // Get first day of year
    var yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1));
    // Calculate full weeks to nearest Thursday
    var weekNo = Math.ceil(( ((d - yearStart) / 86400000) + 1)/7)
    annee = d.getFullYear()
    
    if (weekNo.toString().length==1){
        return  annee.toString() +'-W0'+weekNo.toString();
    }
    else{
        return  annee.toString() +'-W'+weekNo.toString();
    }
}

function getWeekNumberSuivant(d) {
    // Copy date so don't modify original
    d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()+7));
    // Set to nearest Thursday: current date + 4 - current day number
    d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay()||7));
    // Get first day of year
    var yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1));
    // Calculate full weeks to nearest Thursday
    var weekNo = Math.ceil(( ((d - yearStart) / 86400000) + 1)/7)
    annee = d.getFullYear()
    
    if (weekNo.toString().length==1){
        return  annee.toString() +'-W0'+weekNo.toString();
    }
    else{
        return  annee.toString() +'-W'+weekNo.toString();
    }
}

function formatDate(date) {
    var d = new Date(date);
    var mois = '' + (d.getMonth() + 1);
    var jour = '' + d.getDate();
    var annee = d.getFullYear();

    if (mois.length < 2) 
        mois = '0' + mois;
    if (jour.length < 2) 
        jour = '0' + jour;
    return [jour,mois,annee ].join('/');
}
var day =new Date().getDay();
var hours =new Date().getHours();
$(document).ready(function () {
//$('#example-week-input').val(getWeekNumber(new Date()))
//$('#date_jour').val(getDay())
});
















function convertDate(inputFormat) {
    var tmp = inputFormat.split('/');
    var date = tmp[1]+'/'+tmp[0]+'/'+tmp[2];
    return new Date(date)
}
function getDateToday() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; 
    var yyyy = today.getFullYear();
    today = dd+'/'+mm+'/'+yyyy;
    today = convertDate(today)
    return today
}
function getCalculWorkDate(startDate,endDate){
    var count = 0;
    var curDate = startDate;
    while (curDate <= endDate) {
        var dayOfWeek = curDate.getDay();
        if(!((dayOfWeek == 6) || (dayOfWeek == 0)))
            count++;
        curDate.setDate(curDate.getDate() + 1);
    }
    return count;
}
function getWorkDatesCount() {
    var startDate = convertDate(document.getElementById("date_debut").value);
    var endDate = convertDate(document.getElementById("date_fin").value);


    var audit =$('#test :selected').length
   
    $('#nbre_jh_reel').val(Math.abs(getCalculWorkDate(startDate,endDate) * (audit+1)));
    
    $('.auditeurs').val(audit);
    var nbre_jh_reel = document.getElementById("nbre_jh_reel").value;
    var nbre_jh_prevu = document.getElementById("nbre_jh_prevu").value;
    if (nbre_jh_prevu){
        $('#ratio').val(Math.abs(nbre_jh_prevu - nbre_jh_reel));
    }
    else{
        $('#ratio').val("");
    }
}

function getAudit(id){
    var selected = [];
    for (var option of document.getElementById('test'+id).options) {
        if (option.selected) {
        selected.push(option.value);
        }
    }
    $('#auditeurs_final'+id).val(selected);
}
function getWorkDateCount(id) {
    var startDate = convertDate(document.getElementById("date_debut"+id).value);
    var endDate = convertDate(document.getElementById("date_fin"+id).value);

    var audit =$('#test'+id+' :selected').length;

    $('#nbre_jh_reel'+id).val(Math.abs(getCalculWorkDate(startDate,endDate) * audit+1));
    
    $('.auditeurs').val(audit);
    var nbre_jh_reel = document.getElementById("nbre_jh_reel"+id).value;
    var nbre_jh_prevu = document.getElementById("nbre_jh_prevu"+id).value;
    if (nbre_jh_prevu){
        $('#ratio'+id).val(nbre_jh_prevu - nbre_jh_reel);
    }
    else{
        $('#ratio'+id).val("");
    }
}
 

function refreshAt(hour, minutes, seconds) {
    var now = new Date();
    var then = new Date();

    if(now.getHours() > hour ||
    (now.getHours() == hour && now.getMinutes() > minutes) ||
        now.getHours() == hour && now.getMinutes() == minutes && now.getSeconds() >= seconds) {
        then.setDate(now.getDate() + 1);
    }
    then.setHours(hour);
    then.setMinutes(minutes);
    then.setSeconds(seconds);

    var timeout = (then.getTime() - now.getTime());
    setTimeout(function() { window.location.reload(true); }, timeout);
}

function FormatFonction(chaine){
    if (chaine ==="Chef de département"){
        chaine = "Chef_de_departement"
    }
    else if(chaine ==="Chef de service"){
        chaine = "Chef_de_service"
    }
    else if(chaine ==="Data Scientist"){
        chaine = "Data_Scientist"
    }
    return chaine
}