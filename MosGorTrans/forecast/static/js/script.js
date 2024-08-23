function changeImage() {
const item = document.getElementById("ballik");
item.src = "{% static 'images/9.png' %}";
}
changeImage();
console.log(item);