// Disable "Enter" key to prevent submitting the form accidentally
$('html').bind('keypress', function(e) {
   if(e.keyCode === 13 || e.key == 'Enter') {
      return false;
   }
})
let percent_choice=document.getElementById('input-field').value // value chosen by the participant on the dropdown menu
let gender_choice=document.getElementById('gender').value  // value chosen by the participant on input field

function myfunction(){
    let current_task=js_vars.tasks[js_vars.round_number-1] // this is the current task
    decimal_percent= percent_choice/100
    if (current_task=='Ball_bucket_task'){
        document.getElementById('id_Ball_bucket_task').value=decimal_percent
    } else if (current_task=='Count_letters_task'){
            document.getElementById('id_Count_letters_task').value=decimal_percent
    } else if (current_task=='Maze_task'){
            document.getElementById('id_Maze_task').value=decimal_percent
    } else if (current_task=='MRT_task'){
            document.getElementById('id_MRT_task').value=decimal_percent
    } else if (current_task=='Numbers_in_numbers_task'){
            document.getElementById('id_Numbers_in_numbers_task').value=decimal_percent
    } else if (current_task=='NV_task'){
            document.getElementById('id_NV_task').value=decimal_percent
    } else if (current_task=='Word_in_word_task'){
            document.getElementById('id_Word_in_word_task').value=decimal_percent
    } else if (current_task=='Word_order_task'){
            document.getElementById('id_Word_order_task').value=decimal_percent
    } else if (current_task=='Word_puzzle_task'){
            document.getElementById('id_Word_puzzle_task').value=decimal_percent
    } else if (current_task=='Count_numbers_task'){
            document.getElementById('id_Count_numbers_task').value=decimal_percent
    }

    if(gender_choice=="men"){
        document.getElementById("percent_choice").innerHTML = 'Your answer: I think, on average, ' + 'men'.bold() +' correctly answered ' + (percent_choice).toString().bold() + '%'.bold() + ' more questions than'+' women.'.bold()
    }
    else{
        document.getElementById("percent_choice").innerHTML ='Your answer: I think, on average, ' + 'women'.bold() +' correctly answered ' + (percent_choice).toString().bold() + '%'.bold() + ' more questions than'+' men.'.bold()
    }
}


function funDropdownInput(){
    console.log(percent_choice,gender_choice)
    if (gender_choice!="default" and percent_choice!=null){
    myfunction()
    console.log('check 1')
    document.getElementById("next-button").style.display="inline"
    }
    else {document.getElementById("next-button").style.display="none"}
}


function funValueInput(){
    if (gender_choice!="default" and percent_choice!=null){
    myfunction()
    console.log('check 2')
    document.getElementById("next-button").style.display="inline"
    }
    else {document.getElementById("next-button").style.display="none"}

    // the following if statement ensures that if the participant has not chosen a gender he's prompted to choose one

}

function myFunctionReady(){
    document.getElementById("ready-button").style.display="none" // hide the ready-button
    document.getElementById("input-div").style.display="inline" //show the input-div
}