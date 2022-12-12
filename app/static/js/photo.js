function getData() {
    // URL на который будем отправлять GET запрос
    const requestURL = '/get_photo';
    const xhr = new XMLHttpRequest();
    xhr.open('GET', requestURL);
    xhr.responseType = 'json';
    xhr.onload = function() {
        if (xhr.status !== 200) {
            return;
        }
        const response = xhr.response;
        let html = [];
        for (let i = 0, length = response.length; i < length; i++) {
            data = response[i];
            for (key in data){
                html.push('<div class="col-4 gal_col"><a href="'+key+'" target="_blank"><img src="'+data[key]+'" alt="Image" class="img-fluid"></a></div>');
            }
        }
        document.querySelector('.gallery').innerHTML = html.join('');
    }
    xhr.send();
}

getData();