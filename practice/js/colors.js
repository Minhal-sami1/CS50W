document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('button').forEach(function (button) {
        button.onmouseover = function () {
          document.querySelector('h1').style.color = button.dataset.color;
          setInterval(count, 1000);  
        };
    }); 
});