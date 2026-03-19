
function registerFunction(){
   window.location.href = "/register";
}

function loginFunction() {
   window.location.href = "/login";
}


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
   window.location.href = "/dashboard";
}

function loginUser() {
    window.location.href = "/dashboard";
}

// 1. Create a global variable to track status
let passwordReady = false;

function validatePassword() {
    const password = document.getElementById('password').value;
    const hint = document.getElementById('password-hint');

    if (password === "") {
        hint.innerText = "";
        passwordReady = false;
        return;
    }

    // Check conditions
    if (password.length < 8) {
        hint.innerText = "● Must be at least 8 characters";
        passwordReady = false;
    } else if (!/\d/.test(password)) {
        hint.innerText = "● Must include at least one number";
        passwordReady = false;
    } else if (!/[!@#$%^&*]/.test(password)) {
        hint.innerText = "● Must include a special character (@, #, $)";
        passwordReady = false;
    } else {
        hint.innerText = "✔ Password looks strong!";
        hint.style.color = "#2ecc71";
        passwordReady = true; // Only now is it "Ready"
    }

}

function handleFormSubmit(event) {
    if (!passwordReady) {
        event.preventDefault(); // This kills the request before it leaves the browser
        alert("Password is too weak!");
        return false;
    }
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

function loadPage(page, element) { // Added 'element' parameter
    const contentArea = document.getElementById("content-area");

    // --- HIGHLIGHT LOGIC START ---
    // 1. Remove 'active' class from all sidebar links
    const links = document.querySelectorAll('.sidebar ul li a');
    links.forEach(link => link.classList.remove('active'));

    // 2. Add 'active' class to the clicked element (if provided)
    if (element) {
        element.classList.add('active');
    }
    // --- HIGHLIGHT LOGIC END ---

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

async function addData() {
    // 1. Get values from your HTML input IDs
    const facultyData = {
        faculty_id: document.getElementById('newName').value,      // Your ID input
        name: document.getElementById('newCategory').value, 
        ph_no: document.getElementById('newQty').value,       // Your Name input                                         // Default or add a dept input
        sub: document.getElementById('newSub').value            // Your Subject input
                   // Your +91 input
    };

    // Validation: Check if inputs are empty
    if (!facultyData.faculty_id || !facultyData.name) {
        alert("Please fill in at least the ID and Name");
        return;
    }

    try {
        // 2. Send to Python (match the URL to your Flask app)
        const response = await fetch('http://127.0.0.1:5000/add-faculty', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(facultyData)
        });

        const result = await response.json();
        
        if (response.ok) {
            alert(result.message);
            // Optional: Clear the inputs after saving
            document.getElementById('newName').value = "";
            document.getElementById('newCategory').value = "";
            document.getElementById('newQty').value = "";
            document.getElementById('newSub').value = "";
        }
    } catch (error) {
        console.error("Error connecting to server:", error);
        alert("Server is not running. Start your Python script!");
    }
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

window.onload = function () {

    const input = document.getElementById("imageInput");
    const preview = document.getElementById("preview");

    let images = [];

    input.addEventListener("change", function (event) {
        const files = Array.from(event.target.files);

        if (images.length + files.length > 20) {
            alert("Maximum 20 images allowed");
            return;
        }

        files.forEach(file => {
            const reader = new FileReader();

            reader.onload = function (e) {
                images.push(e.target.result);
                displayImages();
            };

            reader.readAsDataURL(file);
        });
    });

    function displayImages() {
        preview.innerHTML = "";

        images.forEach((src, index) => {
            const div = document.createElement("div");
            div.className = "image-box";

            const img = document.createElement("img");
            img.src = src;

            const btn = document.createElement("button");
            btn.innerText = "×";
            btn.className = "remove-btn";

            btn.onclick = function () {
                images.splice(index, 1);
                displayImages();
            };

            div.appendChild(img);
            div.appendChild(btn);
            preview.appendChild(div);
        });
    }

};
