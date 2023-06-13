document.addEventListener("DOMContentLoaded", function() {
    var isLoggedIn = false;
    var loginButton = document.getElementById("loginButton");
    var username = document.getElementById("user_name");
    
    if(loginButton.textContent == "Log in"){
        isLoggedIn = false;
    }
    else{
        isLoggedIn = true;
        // userInfo.innerHTML = "<img src='user_picture.jpg'><span>User Name</span>";
    }

    loginButton.addEventListener("click", function() {
        if(isLoggedIn){
            // redirect to logout page
            window.location.href = "/logout";
        }
        else{
            // redirect to login page
            window.location.href = "/login";
      }

      // Toggle login status
      isLoggedIn = !isLoggedIn;
    });
  });
  