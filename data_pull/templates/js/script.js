// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    var secondsRemaining = 60; // Set the initial time in seconds

    function updateTimer() {
        var minutes = Math.floor(secondsRemaining / 60);
        var seconds = secondsRemaining % 60;

        // Display the timer in the format MM:SS
        document.getElementById('timer').innerHTML = (minutes < 10 ? '0' : '') + minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
    }

    function countdown() {
        updateTimer();
        if (secondsRemaining > 0) {
            secondsRemaining--;
            setTimeout(countdown, 1000); // Update every 1 second
        } else {
            // Reload the page when the timer reaches zero
            location.reload();
        }
    }

    countdown(); // Start the countdown when the page loads
});
