const random_destination = document.getElementById('random_destination');

const destinations = new Array();
destinations[0] = '👚';
destinations[1] = '👕';
destinations[2] = '👗';

function get_randnum(){
    var randNum = Math.floor(Math.random() * destinations.length);
    return randNum;
}

function replace_text(){
    var randNum = get_randnum();
    console.log(randNum);
    random_destination.innerText = destinations[randNum];
    random_destination.className = destinations[randNum];
}

function auto_change(){
    setInterval(replace_text, 3000);
}

function init(){
    auto_change();
}

init();