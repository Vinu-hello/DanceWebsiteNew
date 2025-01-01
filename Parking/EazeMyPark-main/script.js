let slots = document.querySelectorAll(".slot");

let bool = true;

slots.forEach((slot) => {
  slot.addEventListener("click", (el) => {
    el.target.style.backgroundColor = "#FFADB0";
    el.target.style.border = "4px solid red";
    el.target.innerText = "Booked";
    el.target.style.color = "dark-red";
  });
});

let buttons = document.querySelectorAll("button");

buttons.forEach((button) => {
  button.addEventListener("click", (el) => {
    let div = el.target.parentElement.children[0];
    div.style.backgroundColor = "#59e659";
    div.style.border = "4px solid green";
    div.innerText = "Available";
    div.style.color = "dark-green";
  });
});