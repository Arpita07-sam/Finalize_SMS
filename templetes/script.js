let generatedOTP = "";

// Generate OTP
function generateOTP() {
    let phone = document.getElementById("hodPhone")?.value.trim();

    if (!phone) {
        alert("Please enter HOD phone number first!");
        return;
    }

    if (phone.length !== 10) {
        alert("Enter valid 10-digit phone number!");
        return;
    }

    generatedOTP = Math.floor(1000 + Math.random() * 9000).toString();
    alert("Your OTP is: " + generatedOTP);   // Demo only
}

// LOGIN LOGIC
if (document.getElementById("loginForm")) {

    document.getElementById("loginForm").addEventListener("submit", function(event) {
        event.preventDefault();

        let dept = document.getElementById("dept").value.trim().toLowerCase();
        let hodPhone = document.getElementById("hodPhone").value.trim();
        let otp = document.getElementById("otp").value.trim();

        if (generatedOTP === "") {
            document.getElementById("error").innerText = "Please generate OTP first!";
            return;
        }

        if (dept === "cse" && hodPhone === "9392874479" && otp === generatedOTP) {

            sessionStorage.setItem("loggedIn", "true");
            window.location.href = "technician.html";

        } else {
            document.getElementById("error").innerText = "Invalid Details or OTP!";
        }
    });

}

// PROTECT TECHNICIAN PAGE
if (window.location.pathname.includes("technician.html")) {
    if (sessionStorage.getItem("loggedIn") !== "true") {
        window.location.href = "login.html";
    }
}

// Upload Function
function uploadFile() {
    let file = document.getElementById("fileUpload")?.files[0];

    if (file) {
        document.getElementById("uploadMessage").innerText =
            "File '" + file.name + "' uploaded successfully!";
    } else {
        document.getElementById("uploadMessage").innerText =
            "Please select an image first!";
    }
}

// Logout
function logout() {
    sessionStorage.removeItem("loggedIn");
    window.location.href = "login.html";
}