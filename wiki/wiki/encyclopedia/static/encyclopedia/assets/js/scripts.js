function close_side() {
    if(document.querySelector("#sidebar-wrapper").style.width == "250px"){
        document.querySelector("#sidebar-wrapper").style.width = "0px";
    }
    else{document.querySelector("#sidebar-wrapper").style.width = "250px"}
}
window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    const sidebasuToggle = document.body.querySelector('#sidebarunToggle');
    if (sidebarToggle) {
         //Uncomment Below to persist sidebar toggle between refreshes
         if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
             document.body.classList.toggle('sb-sidenav-toggled');
         }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled')); 
        });
    }
    sidebarToggle.onclick = close_side;
    sidebasuToggle.onclick = close_side;
});