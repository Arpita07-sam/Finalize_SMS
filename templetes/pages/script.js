/* OTP GENERATE */

let generatedOTP;

function generateOTP(){
   generatedOTP = Math.floor(1000 + Math.random() * 9000);
   alert("Your OTP: " + generatedOTP);   // for testing
}


/* REGISTER CHECK */

function registerUser(){
   let enteredOTP = document.getElementById("otpInput").value;

   if(enteredOTP == generatedOTP){
      alert("Registered Successfully!");
   }else{
      alert("Wrong OTP");
   }
   window.location.href = "login.html";
}


function validatePassword(){

   let pass = document.getElementById("password").value;

   let pattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/;

   if(pattern.test(pass)){
      alert("Strong password ✅");
   }else{
      alert("Password not strong ❌");
   }

      // demo login check
   alert("Login successful!");

   // go to dashboard
   window.location.href = "main.html";
}



/* SHOW PASSWORD */

function togglePassword(){
   let pass = document.getElementById("password");
   let btn = document.querySelector(".show-btn");

   if(pass.type === "password"){
      pass.type = "text";
      btn.innerText = "Hide";
   }else{
      pass.type = "password";
      btn.innerText = "Show";
   }
}


/* LIVE PASSWORD CHECK */

function checkPassword(){

let pass = document.getElementById("password").value;

document.getElementById("length").style.color =
pass.length >= 8 ? "green" : "red";

document.getElementById("upper").style.color =
/[A-Z]/.test(pass) ? "green" : "red";

document.getElementById("number").style.color =
/[0-9]/.test(pass) ? "green" : "red";

document.getElementById("special").style.color =
/[@$!%*?&]/.test(pass) ? "green" : "red";

}

function logout(){
   window.location.href = "login.html";
}

function toggleMenu(){

   let sidebar = document.getElementById("sidebar");
   sidebar.classList.toggle("active");

}

document.querySelector('.category-header').addEventListener('click', function() {
    this.parentElement.classList.toggle('active');
    
    // Toggle showing/hiding the submenu
    const submenu = this.nextElementSibling;
    if (submenu.style.display === "block") {
        submenu.style.display = "none";
    } else {
        submenu.style.display = "block";
    }
});

function handleMultipleUpload(event) {
    const files = event.target.files;
    const container = document.getElementById('image-list');

    for (let i = 0; i < files.length; i++) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            // Create wrapper
            const wrapper = document.createElement('div');
            wrapper.classList.add('image-wrapper');

            // Create image
            const img = document.createElement('img');
            img.src = e.target.result;
            img.classList.add('uploaded-image-rect');

            // Create remove mark
            const removeBtn = document.createElement('button');
            removeBtn.innerHTML = '×';
            removeBtn.classList.add('remove-mark');
            
            // Remove functionality
            removeBtn.onclick = function() {
                wrapper.remove();
            };

            wrapper.appendChild(img);
            wrapper.appendChild(removeBtn);
            container.appendChild(wrapper);
        }
        
        reader.readAsDataURL(files[i]);
    }
    // Clear input so you can re-upload the same image if needed
    event.target.value = "";
}




