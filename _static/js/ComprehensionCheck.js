// Disable "Enter" key to prevent submitting the form accidentally
$('html').bind('keypress', function(e) {
   if(e.keyCode === 13 || e.key == 'Enter') {
      return false;
   }
})

function myFunction(){
    // this function is called when the participant interacts with the 2 input fields
    document.getElementById("check-answer-button").style.display="inline"
    comparison_answer=document.getElementById('comparison-field').value // second field
    group_B_answer=document.getElementById('groupB-field').value // first field

    //the following if statement ensures that if the participant has not chosen a group he's prompted to choose one
    if (group_B_answer=="default" && comparison_answer=="default"){
        document.getElementById("percent_choice").innerHTML = "Answer the questions to continue."
    }
    else{
        document.getElementById("percent_choice").innerHTML = "Your answer: I think, group B answered "+ group_B_answer.toString().bold() + " many questions correctly and group A answered " +
        comparison_answer.toString().bold() +  " many more questions correctly than to group B."
    }
    
    // if the participant answers the question correctly we assign 1 to the hidden input field, else 0
    if (comparison_answer == '6' && group_B_answer == '7'){
        document.getElementById('id_ComprehensionCheck_task').value = '1'
        console.log(document.getElementById('id_ComprehensionCheck_task').value)
    } else {document.getElementById('id_ComprehensionCheck_task').value = '0'
        console.log(document.getElementById('id_ComprehensionCheck_task').value)
    }
}

function myFunctionReady(){
    // this function is called when the participant clicks on the ready-button
    document.getElementById("ready-button").style.display="none" //hide the ready-button
    document.getElementById("input-div").style.display="inline" //show the input-div
}