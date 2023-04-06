<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $name = $_POST["name"];
  $email = $_POST["email"];
  $subject = $_POST["subject"];
  $message = $_POST["message"];
  
  $to = "rfritz002@gmail.com"; // replace with your email address
  $subject = "New message from your website";
  $body = "Name: $name\nEmail: $email\nSubject: $subject\nMessage: $message";
  
  if (mail($to, $subject, $body)) {
    echo "Thank you for your message!";
  } else {
    echo "Sorry, there was an error sending your message. Please try again later.";
  }
}
?>
