let elements = document.querySelectorAll('.rating')[0];
let attr = ["one", "two", "three", "four", "five"]
for (let i = 0; i < elements.children.length; i++) {
    each = elements.children[i]
    each.setAttribute("id", attr[i])
}




for (let n = 0; n < attr.length; n++) {
    let element = document.getElementById(attr[n])
    let title = document.getElementById("main-title").innerHTML
    let username = document.getElementById("username").innerHTML

    element.addEventListener('click', function() {
        let xhttp = new XMLHttpRequest();
        let fd = new FormData();
        let data = {
            type: 'POST',
            contentType: 'application/json',
            'username': username,
            'title': title,
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