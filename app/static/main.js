
      const navLinks = document.querySelectorAll(".nav__link");

      navLinks.forEach((link) => {
        link.addEventListener("click", () => {
          navLinks.forEach((otherLink) =>
            otherLink.classList.remove("active-link")
          );
          link.classList.add("active-link");
        });

      /**
       * @description Shows the cookie banner
       */
      function showCookieBanner() {
        let cookieBanner = document.getElementById("cb-cookie-banner");
        cookieBanner.style.display = "block";
      }

      /**
       * @description Hides the Cookie banner and saves the value to localstorage
       */
      function hideCookieBanner() {
        localStorage.setItem("cb_isCookieAccepted", "yes");

        let cookieBanner = document.getElementById("cb-cookie-banner");
        cookieBanner.style.display = "none";

        // Call the set_cookie view using AJAX
        fetch("/set-cookie/");
        fetch("/read-cookie/")
          .then((response) => response.json())
          .then((data) => {
            console.log(data.message); // Print the response from the server
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      }

      /**
       * @description Checks the localstorage and shows Cookie banner based on it.
       */
      function initializeCookieBanner() {
        let isCookieAccepted = localStorage.getItem("cb_isCookieAccepted");
        if (isCookieAccepted === null) {
          localStorage.setItem("cb_isCookieAccepted", "no");
          showCookieBanner();
        }
        if (isCookieAccepted === "no") {
          showCookieBanner();
        }
      }

      // Assigning values to window object
      window.onload = initializeCookieBanner();
      window.cb_hideCookieBanner = hideCookieBanner;


      // Function to start both carousels in sync
      function startCarouselsInSync() {
        $("#carouselRedmi, #carouselPoco").carousel({
          interval: 3000, // Set the interval time for sliding (e.g., 3000ms = 3 seconds)
          pause: "false",
        });
      }

      // Start both carousels in sync when the document is ready
      $(document).ready(function () {
        startCarouselsInSync();
      });


  // Function to toggle between light and dark mode
  function toggleTheme() {
    const body = $('body');
    if (body.hasClass('light-mode')) {
      body.removeClass('light-mode').addClass('dark-mode');
      localStorage.setItem('theme', 'dark'); // Save theme preference in Local Storage
    } else {
      body.removeClass('dark-mode').addClass('light-mode');
      localStorage.setItem('theme', 'light'); // Save theme preference in Local Storage
    }
  }

  // Add event listener to the theme toggle button
  $(document).ready(function () {
    $('#themeToggle').on('change', function () {
      toggleTheme();
    });

    // Load the user's preferred theme
    function loadTheme() {
      const theme = localStorage.getItem('theme');
      if (theme === 'dark') {
        $('body').addClass('dark-mode');
        $('#themeToggle').prop('checked', true);
      } else {
        $('body').addClass('light-mode');
        $('#themeToggle').prop('checked', false);
      }
    }

    loadTheme();
  });

      document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener("click", function (e) {
          e.preventDefault();

          const target = document.querySelector(this.getAttribute("href"));
          const offset = 50; // Adjust the offset value as needed
          const topPosition = target.offsetTop - offset;

          window.scrollTo({
            top: topPosition,
            behavior: "smooth",
          });
        });
      });


      //Get the button
      let mybutton = document.getElementById("btn-back-to-top");

      // When the user scrolls down 20px from the top of the document, show the button
      window.onscroll = function () {
        scrollFunction();
      };

      function scrollFunction() {
        if (
          document.body.scrollTop > 20 ||
          document.documentElement.scrollTop > 20
        ) {
          mybutton.style.display = "block";
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
