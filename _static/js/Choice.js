// Disable "Enter" key to prevent submitting the form accidentally
$('html').bind('keypress', function(e) {
   if(e.keyCode === 13 || e.key == 'Enter') {
      return false;
   }
})

// Disable mousewheel from changing the input field, make sure to add noscroll class to the input field.
document.addEventListener("wheel", function(event){
    if(document.activeElement.type === "number" &&
       document.activeElement.classList.contains("noscroll"))
    {
        document.activeElement.blur();
    }
});



function myfunction(){
    let difference_choice=document.getElementById('input-field').value // value chosen by the participant on input field
    let gender_choice=document.getElementById('gender').value  // value chosen by the participant on the dropdown menu

    if (gender_choice == 'men'){
        percent_choice=difference_choice/(10-difference_choice/2)}
    else if(gender_choice == 'women'){
        percent_choice=-difference_choice/(10+difference_choice/2)}
    else {print("error in percent_choice")}


    let current_task=js_vars.tasks[js_vars.round_number-1] // this is the current task
    if (current_task=='Ball_bucket_task'){
        document.getElementById('id_Ball_bucket_task').value=percent_choice
    } else if (current_task=='Count_letters_task'){
            document.getElementById('id_Count_letters_task').value=percent_choice
    } else if (current_task=='Maze_task'){
            document.getElementById('id_Maze_task').value=percent_choice
    } else if (current_task=='MRT_task'){
            document.getElementById('id_MRT_task').value=percent_choice
    } else if (current_task=='Numbers_in_numbers_task'){
            document.getElementById('id_Numbers_in_numbers_task').value=percent_choice
    } else if (current_task=='NV_task'){
            document.getElementById('id_NV_task').value=percent_choice
    } else if (current_task=='Word_in_word_task'){
            document.getElementById('id_Word_in_word_task').value=percent_choice
    } else if (current_task=='Word_order_task'){
            document.getElementById('id_Word_order_task').value=percent_choice
    } else if (current_task=='Word_puzzle_task'){
            document.getElementById('id_Word_puzzle_task').value=percent_choice
    } else if (current_task=='Count_numbers_task'){
            document.getElementById('id_Count_numbers_task').value=percent_choice
    }

    if(gender_choice=="men"){
        document.getElementById("answer-paragraph").innerHTML = 'Your answer: I think, on average, ' + 'men'.bold() +' correctly answered ' + (difference_choice).toString().bold() +  ' more questions than'+' women. '.bold()+
        "In other words, on average, men answered " +(10+difference_choice/2).toString().bold() + " questions, women answered " + (10-difference_choice/2).toString().bold()  +  " questions correctly."
    }
    else{
        document.getElementById("answer-paragraph").innerHTML ='Your answer: I think, on average, ' + 'women'.bold() +' correctly answered ' + (difference_choice).toString().bold() +  ' more questions than'+' men.'.bold()+
        "In other words, on average, men answered " +(10-difference_choice/2).toString().bold() + " questions, women answered " + (10+difference_choice/2).toString().bold()  +  " questions correctly."
    }
}


function funDropdownInput(){
    let difference_choice=document.getElementById('input-field').value // value chosen by the participant on the dropdown menu
    let gender_choice=document.getElementById('gender').value  // value chosen by the participant on input field

    console.log(difference_choice,gender_choice)
    if (gender_choice!="default" && difference_choice!=null){
    myfunction()
    document.getElementById("next-button").style.display="inline"
    }
    else {document.getElementById("next-button").style.display="none"}
}


function funValueInput(){
    let difference_choice=document.getElementById('input-field').value // value chosen by the participant on the dropdown menu
    let gender_choice=document.getElementById('gender').value  // value chosen by the participant on input field

    if (gender_choice!="default" && difference_choice!=null){
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