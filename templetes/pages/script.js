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


function loadPage(page) {

    const contentArea = document.getElementById("content-area");

    // default dashboard view
    if (page === "dashboard") {
        contentArea.innerHTML = `
            <div class="data-table">
                <h3 class="page-header">Upload the image here</h3>

                <div class="image-uploader-grid">
                    <div id="image-list" class="image-list-container"></div>

                    <label class="add-image-btn">
                        <span>+</span>
                        <input type="file" id="multi-upload" accept="image/*" multiple onchange="handleMultipleUpload(event)">
                    </label>
                </div>
                <br>
                <p>Your latest project updates will appear here.</p>
            </div>
        `;
        return;
    }

    // load external html inside dashboard
    fetch(page)
        .then(res => res.text())
        .then(data => {
            contentArea.innerHTML = data;
        })
        .catch(err => {
            contentArea.innerHTML = "<h2>Page not found</h2>";
        });
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

function submitToDB() {
   // 1. Grab values from the input fields
   const name = document.getElementById('newName').value;
   const category = document.getElementById('newCategory').value;
   const qty = document.getElementById('newQty').value;

   if(!name || !category || !qty) {
      alert("Please fill in all fields");
      return;
   }

   // 2. Logic to send to your database (via Fetch API later)
   console.log("Sending to DB:", { name, category, qty });

   // For now, let's just clear the inputs
   document.getElementById('newName').value = '';
   document.getElementById('newCategory').value = '';
   document.getElementById('newQty').value = '';
   
   alert("Ready to connect to backend!");
}

function addData() {
    alert("Add clicked");
}

function editData() {
    alert("Edit clicked");
}

function deleteData() {
    alert("Delete clicked");
}

function uploadData() {
    alert("Upload clicked");
}





