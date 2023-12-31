const navLinks = document.querySelectorAll(".nav__link");

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    navLinks.forEach((otherLink) =>
      otherLink.classList.remove("active-link")
    );
    link.classList.add("active-link");
  });
});


// Javascript code for back to top button :
//Get the button
document.addEventListener("DOMContentLoaded", function() {
  var mybutton = document.getElementById("btn-back-to-top");

  if (mybutton) {
    function scrollFunction() {
      if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "flex";
      } else {
        mybutton.style.display = "none";
      }
    }

    // When the user clicks on the button, scroll to the top of the document
    mybutton.addEventListener("click", backToTop);

    function backToTop() {
      document.body.scrollTop = 0;
      document.documentElement.scrollTop = 0;
    }

    // Attach the scrollFunction to the window's scroll event
    window.onscroll = scrollFunction;
  }
});
