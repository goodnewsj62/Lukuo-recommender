let secondElements = document.querySelectorAll('.js-rating');
let value = 0;

for (let j = 0; j < secondElements.length; j++) {
    let getElements = secondElements[j];

    let attrb = []

    for (let thresh = value + 5; value < thresh; value++) {
        attrb.push(value)
    }



    //set attribute for children (list) one after the other
    for (let n = 0; n < getElements.children.length; n++) {
        let element = getElements.children[n];
        let secondTitle = document.querySelectorAll('.js-grab')[j]
        secondTitle = secondTitle.innerHTML
        let username = document.getElementById("username").innerHTML
        console.log();



        element.addEventListener('click', function() {
            let xhttp = new XMLHttpRequest();
            let fd = new FormData();
            let data = {
                type: 'POST',
                contentType: 'application/json',
                'username': username,
                'title': secondTitle,
                'level': n + 1

            };

            for (name in data) {
                fd.append(name, data[name]);
            }

            xhttp.open('POST', 'http://localhost:5000/rating', true);

            xhttp.onload = function() {
                if (xhttp.status == 200) {
                    console.log(element);
                }
            }

            xhttp.send(fd);
        });
    }
}