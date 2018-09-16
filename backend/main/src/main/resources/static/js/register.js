function register() {
    var firstName = document.getElementById('firstName').value;
    var lastName = document.getElementById('lastName').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var passwordRepeat = document.getElementById('passwordRepeat').value;

    if (password != passwordRepeat) {
        alert('Пароли не совпадают');
        return;
    }

    password = MD5(password);
    var requestUrl = 'http://localhost:8080/register';

    $.ajax({
        url: requestUrl,
        method: 'POST',
        data: {
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password
        }
    }).then(function(data) {
        window.location.replace("/avia");
        // obj.hasOwnProperty('field')
    }).catch(function(data) {
        alert("Ошибка");
    });
}