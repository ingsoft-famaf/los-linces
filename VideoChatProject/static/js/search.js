function change(id) {
    var elem = document.getElementById(id);
    var elemClasses = elem.classList;

    console.log(elem.innerHTML);
    if (elem.innerHTML=="Add friend"){
        elem.innerHTML = "Cancel request";
        elemClasses.remove('btn-success');
        elemClasses.add('btn-danger');
    } else {
        elem.innerHTML = "Add friend";
        elemClasses.remove('btn-danger');
        elemClasses.add('btn-success');
    }
    elem.blur();
}