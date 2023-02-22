// Disable "Enter" key to prevent submitting the form accidentally
$('html').bind('keypress', function(e) {
   if(e.keyCode === 13 || e.key == 'Enter') {
      return false;
   }
})

let Allowed_number_attempts=js_vars.Allowed_number_attempts

window.onload = function(){
    var attempts_left=localStorage.getItem('attempts_left')

    if(attempts_left==null){
        localStorage.setItem("attempts_left", Allowed_number_attempts)
    }
    console.log(attempts_left)
}



function myFunction(){
    document.getElementById("check-answer-button").style.display="inline"
    comparison_answer=document.getElementById('comparison-field').value // second answer
    group_B_answer=document.getElementById('groupB-field').value // first answer

    //the following if statement ensures that if the participant has not chosen a group he's prompted to choose one
    if (group_B_answer=="default" && comparison_answer=="default"){
        document.getElementById("percent_choice").innerHTML = "Answer the questions to continue."
    }
    else{
        document.getElementById("percent_choice").innerHTML = "Your answer: I think, group B answered "+ group_B_answer.toString().bold() + " many questions correctly and group A answered " +
        comparison_answer.toString().bold() +  " many more questions correctly than to group B."
    }
}

function myFunctionReady(){
    document.getElementById("ready-button").style.display="none" //hide the ready-button
    document.getElementById("input-div").style.display="inline" //show the input-div
}

function checkAnswer(){
    var attempts_left=localStorage.getItem('attempts_left')
    document.getElementById("check-answer-button").style.display="none"

    if (group_B_answer=="7" && comparison_answer=="6"){
    document.getElementById("answer-validity").innerHTML='Correct!'.bold()
    document.getElementById("next-button").style.display="inline"
    } else {
    attempts_left--
    if (attempts_left<=0){
    document.getElementById("answer-validity").innerHTML='Incorrect Answer! You have no more attempts left.'.bold() + ' Correct answer was: "Group B 7 questions correctly so group A answered 6 more than group B"'
    document.getElementById("next-button").style.display="inline"
   }
    else {
    document.getElementById("answer-validity").innerHTML='Incorrect Answer! You have '.bold() + attempts_left.toString().bold() + ' more attempt(s) left. Please try again'.bold()
    }
    }
    localStorage.setItem("attempts_left", attempts_left)
    document.getElementById("id_attempts").value=attempts_left
}

