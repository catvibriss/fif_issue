function changeImage() {
const item = document.getElementsByClassName("balls");
item.src = "{% static 'images/9.png' %}";
}
changeImage();