(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
// Login and Registration JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Handle login form submission
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleLogin();
        });
        
        document.getElementById('sendOtpBtn').addEventListener('click', function() {
            sendOtp('email');
        });
    }
    
    // Handle admin login form submission
    const adminLoginForm = document.getElementById('adminLoginForm');
    if (adminLoginForm) {
        adminLoginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleAdminLogin();
        });
        
        document.getElementById('sendOtpBtn').addEventListener('click', function() {
            sendOtp('email');
        });
    }
    
    // Handle registration form submission
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleRegistration();
        });
        
        document.getElementById('sendEmailOtpBtn').addEventListener('click', function() {
            sendOtp('email');
        });
        
        document.getElementById('sendPhoneOtpBtn').addEventListener('click', function() {
            sendOtp('phone');
        });
        
        // Auto-calculate age based on DOB
        document.getElementById('dob').addEventListener('change', function() {
            const dob = new Date(this.value);
            const today = new Date();
            const age = Math.floor((today - dob) / (365.25 * 24 * 60 * 60 * 1000));
            document.getElementById('age').value = age;
        });
    }
});

// Function to send OTP
async function sendOtp(type) {
    const email = document.getElementById('email')?.value || document.getElementById('email').value;
    let contactNumber = null;
    
    if (type === 'phone') {
        contactNumber = document.getElementById('contactNumber')?.value;
        if (!contactNumber) {
            alert('Please enter your contact number');
            return;
        }
    }
    
    if (!email && type === 'email') {
        alert('Please enter your email');
        return;
    }
    
    try {
        const response = await fetch('/otp/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: type === 'email' ? email : undefined,
                contact_number: type === 'phone' ? contactNumber : undefined
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            if (data.dev_otp) {
                // Show OTP in alert when email/SMS is not configured
                alert(`OTP sent! Since email/SMS is not configured, your OTP is: ${data.dev_otp}\n\nPlease use this OTP to verify.`);
                console.log(`[DEV] OTP for ${type}: ${data.dev_otp}`);
            } else {
                alert(`OTP sent successfully to your ${type}!`);
            }
        } else {
            const errorMessage = data.detail || data.message || 'Unknown error';
            alert(`Failed to send OTP: ${errorMessage}`);
        }
    } catch (error) {
        console.error('Error sending OTP:', error);
        alert('Error sending OTP. Please try again.');
    }
}

// Function to handle user login
async function handleLogin() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const otp = document.getElementById('otp').value;
    
    // First verify OTP
    try {
        const otpResponse = await fetch('/otp/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                otp: otp
            })
        });
        
        if (!otpResponse.ok) {
            const otpData = await otpResponse.json();
            alert(`OTP verification failed: ${otpData.detail}`);
            return;
        }
        
        // If OTP is verified, proceed with login
        const response = await fetch(`/login?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
        
        if (response.ok) {
            const data = await response.json();
            // Store token in localStorage
            localStorage.setItem('token', data.token);
            localStorage.setItem('role', data.role);
            
            // Redirect based on role
            if (data.role === 'admin') {
                window.location.href = '/admin.html';
            } else {
                // User redirects to voting page
                window.location.href = '/index.html';
            }
        } else {
            const errorData = await response.json();
            alert(`Login failed: ${errorData.detail}`);
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please try again.');
    }
}

// Function to handle admin login
async function handleAdminLogin() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const otp = document.getElementById('otp').value;
    
    // First verify OTP
    try {
        const otpResponse = await fetch('/otp/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                otp: otp
            })
        });
        
        if (!otpResponse.ok) {
            const otpData = await otpResponse.json();
            alert(`OTP verification failed: ${otpData.detail}`);
            return;
        }
        
        // If OTP is verified, proceed with login
        const response = await fetch(`/login?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
        
        if (response.ok) {
            const data = await response.json();
            
            // Check if user is admin
            if (data.role !== 'admin') {
                alert('You are not authorized to access the admin panel.');
                return;
            }
            
            // Store token in localStorage
            localStorage.setItem('token', data.token);
            localStorage.setItem('role', data.role);
            
            // Redirect to admin dashboard
            window.location.href = '/admin.html';
        } else {
            const errorData = await response.json();
            alert(`Login failed: ${errorData.detail}`);
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please try again.');
    }
}

// Function to handle user registration
async function handleRegistration() {
    const formData = {
        firstName: document.getElementById('firstName').value,
        middleName: document.getElementById('middleName').value,
        lastName: document.getElementById('lastName').value,
        aadhar: document.getElementById('aadhar').value,
        voterId: document.getElementById('voterId').value,
        dob: document.getElementById('dob').value,
        age: document.getElementById('age').value,
        gender: document.getElementById('gender').value,
        contactNumber: document.getElementById('contactNumber').value,
        email: document.getElementById('email').value,
        address: document.getElementById('address').value,
        password: document.getElementById('password').value,
        confirmPassword: document.getElementById('confirmPassword').value
    };
    
    // Verify passwords match
    if (formData.password !== formData.confirmPassword) {
        alert('Passwords do not match!');
        return;
    }
    
    // Verify OTPs
    const emailOtp = document.getElementById('emailOtp').value;
    const phoneOtp = document.getElementById('phoneOtp').value;
    
    try {
        // Verify email OTP
        const emailOtpResponse = await fetch('/otp/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: formData.email,
                otp: emailOtp
            })
        });
        
        if (!emailOtpResponse.ok) {
            const otpData = await emailOtpResponse.json();
            alert(`Email OTP verification failed: ${otpData.detail}`);
            return;
        }
        
        // Verify phone OTP
        const phoneOtpResponse = await fetch('/otp/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contact_number: formData.contactNumber,
                otp: phoneOtp
            })
        });
        
        if (!phoneOtpResponse.ok) {
            const otpData = await phoneOtpResponse.json();
            alert(`Phone OTP verification failed: ${otpData.detail}`);
            return;
        }
        
        // If both OTPs are verified, proceed with registration
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            alert('Registration successful! You can now login.');
            window.location.href = '/login.html';
        } else {
            const errorData = await response.json();
            alert(`Registration failed: ${errorData.detail}`);
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration failed. Please try again.');
    }
}
},{}]},{},[1]);
