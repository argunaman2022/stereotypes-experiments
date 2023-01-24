function myFunction(){
    document.getElementById("next-button").style.display="inline" {# show the next button#}

    {# store the chosen value of the slider in var "hischoice"#}
    hischoice=document.getElementById('slider_choice_django').value {# value chosen by the participant on the slider #}
    hischoice_percentage= Math.round(parseFloat(hischoice)*100) {# in percentage points #}

    let round=js_vars.round_number {# current round number #}
    let tasks=js_vars.tasks {# this is a list of tasks#}
    let current_task=tasks[round-1] {# this is the current task#}
    console.log(current_task)

    if (current_task=='Ball_bucket_task'){
            console.log(current_task)
            document.getElementById('id_Ball_bucket_task').value=hischoice

    } else if (current_task=='Count_letters_task'){
            console.log(current_task)
            document.getElementById('id_Count_letters_task').value=hischoice

    } else if (current_task=='Maze_task'){
            console.log(current_task)
            document.getElementById('id_Maze_task').value=hischoice

    } else if (current_task=='MRT_task'){
            console.log(current_task)
            document.getElementById('id_MRT_task').value=hischoice

    } else if (current_task=='Numbers_in_numbers_task'){
            console.log(current_task)
            document.getElementById('id_Numbers_in_numbers_task').value=hischoice

    } else if (current_task=='NV_task'){
            console.log(current_task)
            document.getElementById('id_NV_task').value=hischoice

    } else if (current_task=='Word_in_word_task'){
            console.log(current_task)
            document.getElementById('id_Word_in_word_task').value=hischoice

    } else if (current_task=='Word_order_task'){
            console.log(current_task)
            document.getElementById('id_Word_order_task').value=hischoice

    } else if (current_task=='Word_puzzle_task'){
            console.log(current_task)
            document.getElementById('id_Word_puzzle_task').value=hischoice
    } else {
            console.log(current_task)
            document.getElementById('id_Count_numbers_task').value=hischoice
    }

    if(hischoice_percentage>0){
    document.getElementById("hischoice").innerHTML = 'I think, on average, ' + 'men'.bold() +' correctly answered ' + (hischoice_percentage).toString().bold() + '%'.bold() + ' more questions than'+' women.'.bold()
    }
    else{
    document.getElementById("hischoice").innerHTML ='I think, on average, ' + 'women'.bold() +' correctly answered ' + (-hischoice_percentage).toString().bold() + '%'.bold() + ' more questions than'+' men.'.bold()
    }

}

function myFunctionReady(){
    document.getElementById("ready-button").style.display="none" {# hide the ready-button#}
    document.getElementById("slider-div").style.display="inline" {#show the slider-div#}
}
