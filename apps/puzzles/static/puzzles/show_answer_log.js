let answer_log = document.getElementById("answer_log")

document.getElementById("answer_log_h3").addEventListener("click", () => {
	if(answer_log.hasAttribute("hidden")){
		answer_log.removeAttribute("hidden")
	} else {
		answer_log.setAttribute("hidden", true)
	}
})