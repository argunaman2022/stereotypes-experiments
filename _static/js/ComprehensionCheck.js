// Disable "Enter" key to prevent submitting the form accidentally
$('html').bind('keypress', function(e) {
   if(e.keyCode === 13 || e.key == 'Enter') {
      return false;
   }
})

function myFunction(){
    document.getElementById("check-answer-button").style.display="inline"

    percent_choice=document.getElementById('input-field').value //value chosen by the participant on the slider
    group_choice=document.getElementById('group').value


    //the following if statement ensures that if the participant has not chosen a group he's prompted to choose one
    if (group_choice=="default"){
        document.getElementById("percent_choice").innerHTML = "Choose a value from the dropdown menu to continue"
    }
    else{
        decimal_percent= percent_choice/100
        document.getElementById('id_ComprehensionCheck_task').value=decimal_percent

    if(group_choice=="group A"){
        document.getElementById("percent_choice").innerHTML = 'Your answer: I think, on average, ' + 'Group A'.bold() +' correctly answered ' + (percent_choice).toString().bold() + '%'.bold() + ' more questions than'+' Group B.'.bold()
    }
    else{
        document.getElementById("percent_choice").innerHTML ='Your answer: I think, on average, ' + 'Group B'.bold() +' correctly answered ' + (percent_choice).toString().bold() + '%'.bold() + ' more questions than'+' Group A.'.bold()
    }
    }
}

function myFunctionReady(){
    document.getElementById("ready-button").style.display="none" //hide the ready-button
    document.getElementById("input-div").style.display="inline" //show the input-div
}

function checkAnswer(){
    document.getElementById("check-answer-button").style.display="none"
    console.log(group_choice, percent_choice)
    if (group_choice=="group B" && percent_choice=="50"){
    document.getElementById("answer-validity").innerHTML='Correct!'.bold()
    document.getElementById("next-button").style.display="inline"
    } else {
    document.getElementById("answer-validity").innerHTML='Incorrect Answer! Try again?'.bold()
    document.getElementById("next-button").style.display="none"
    }
}