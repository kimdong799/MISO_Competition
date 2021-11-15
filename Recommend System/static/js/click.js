const label1 = document.querySelector('.type_label1');
const label2 = document.querySelector('.type_label2');
const label3 = document.querySelector('.type_label3');

const CLICKED_CLASS = "clicked";

function handleClick1(){
    label1.classList.add(CLICKED_CLASS);
    label3.classList.remove(CLICKED_CLASS);
    label2.classList.remove(CLICKED_CLASS);
}
function handleClick2(){
    label1.classList.remove(CLICKED_CLASS);
    label3.classList.remove(CLICKED_CLASS);
    label2.classList.add(CLICKED_CLASS);
}
function handleClick3(){
    label1.classList.remove(CLICKED_CLASS);
    label3.classList.add(CLICKED_CLASS);
    label2.classList.remove(CLICKED_CLASS);
}



function init(){
    label1.addEventListener("click", handleClick1);
    label2.addEventListener("click", handleClick2);
    label3.addEventListener("click", handleClick3);
}
init();