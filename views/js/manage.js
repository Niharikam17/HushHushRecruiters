$(document).ready(function() {
	$("#execute-process").click(executeRecruitingProcess);
});

function executeRecruitingProcess() {
    var jsonData = {
	                   "scrape_stackoverflow_data": $("#cond-one").is(":checked"),
	                   "fetch_data_from_stackexchange_api": $("#cond-two").is(":checked"),
	                   "train_model_again": $("#cond-three").is(":checked"),
	                   "fetch_top_users": $("#cond-four").is(":checked"),
	                   "send_email_to_user": $("#cond-five").is(":checked"),
	                   "users_count": parseInt($("#user-count").val())
                   }

    $.ajax({
		url: "http://127.0.0.1:5050/execute_recruiting_process",
		type: "POST",
		data: JSON.stringify(jsonData),
		contentType:"application/json",
		dataType: 'json',
		success: function(response) {
			console.log(response)
		}
	});
}