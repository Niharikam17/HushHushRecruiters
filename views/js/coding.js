$(document).ready(function() {
	$("#submit-challenge").click(submit_challenge);

	try {
		var url = new URL(location.href);
	    var timeLimit = parseInt(url.searchParams.get("time_limit")) * 1000;

		var remainingTime = timeLimit - (new Date()).getTime();

		if(remainingTime <= 0) {
			$("#timer-container").html("Your Exam Session has expired. Better luck next time!");
			$("#timer-container").css("color", "red");
			$("#submit-challenge").remove();
		} else {
			startTimer(remainingTime / 1000);
		}
	} catch(err) {
		// PASS
	}
});

function startTimer(seconds) {
  let timer = seconds;

  const intervalId = setInterval(function() {
    timer--;

    $("#timer").html(getRemainingTime(timer));

    if (timer <= 0) {
      location.reload()
    }

  }, 1000);
}

function getRemainingTime(seconds) {
  const hours = Math.floor(seconds / 3600).toString().padStart(2, '0');
  const minutes = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
  const remainingSeconds = Math.floor((seconds % 60)).toString().padStart(2, '0');

  return `${hours}:${minutes}:${remainingSeconds}`;
}



function submit_challenge() {
	var ansOne = $("#question-1").val();
	var ansTwo = $("#question-2").val();
	var ansThree = $("#question-3").val();

	var finalAns = ansOne + ansTwo + ansThree;

	var url = new URL(location.href);
    var accountId = url.searchParams.get("account_id");

	var jsonData = {
	                   "final_answer": finalAns,
	                   "account_id": accountId
                   }

    $.ajax({
		url: "http://127.0.0.1:5050/submit_exam",
		type: "POST",
		data: JSON.stringify(jsonData),
		contentType:"application/json",
		dataType: 'json',
		success: function(response) {
			if (response.message) {
				location.href = "thank_you.html";
			} else {
				alert("Something went wrong !");
			}
		}
	});
}