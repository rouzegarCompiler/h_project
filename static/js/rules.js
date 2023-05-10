const buttons = document.querySelectorAll(".toggle-button");
const texts = document.querySelectorAll(".toggle-text");

for (let i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener("click", function() {
    if (texts[i].style.display === "none") {
      texts[i].style.display = "block";
    } else {
      texts[i].style.display = "none";
    }
  });
}
