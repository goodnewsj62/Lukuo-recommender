title = document.querySelectorAll('#js-info');
for (let j = 0; j < title.length; j++) {
    let mainElement = title[j];
    let element = document.querySelectorAll('#js-title')[j]


    if (element.innerHTML.length > 15 && element.innerHTML.length < 25) {
        mainElement.classList.add('music-info');
    }
    if (element.innerHTML.length > 24) {
        mainElement.classList.add('toggle');
    }

}