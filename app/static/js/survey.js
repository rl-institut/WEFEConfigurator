function deselect(elm) {
    if (elm.checked == true) {
    elm.click();
    }
}

function triggerSubQuestion(new_value,subQuestionMapping){
    console.log("Trigger Sub Question");
    var stray = [];
    if(new_value.type == "checkbox"){
        var checkBoxes = new_value.parentElement.parentElement.querySelectorAll('input[type="checkbox"]'); // get all the check box
        checkBoxes.forEach(item => {if (item.checked){stray.push(item.value);}})
    }
    else{
        var array_opts = Object.values(new_value.selectedOptions);
        stray = array_opts.map((o)=> o.value);
    }
    // selected options
    console.log("selected options", stray);


    var sub_questions = [];
    stray.filter((r) => {
        // select only potential subquestions
        return r in subQuestionMapping;
    }).map((o)=>{
      // if there are more than one subquestion, expands their numbers
        if( typeof subQuestionMapping[o] != "string"){
            subQuestionMapping[o].map((e)=>{sub_questions.push(e);});
        }
        else{sub_questions.push(subQuestionMapping[o]);}
    });
    console.log("selected_values", sub_questions);

    for (let key in subQuestionMapping) {
        if(typeof subQuestionMapping[key] === 'string' || subQuestionMapping[key] instanceof String){
            var q_id = [subQuestionMapping[key]];
        }
        else{q_id=subQuestionMapping[key]}

        console.log("ids", q_id)

        // loop over the subquestions
        for (let key_i in q_id){
            var subQuestionDiv = document.getElementById("div_id_criteria_" + q_id[key_i]);
            console.log("displaying subquestions for" + subQuestionDiv)
            // TODO maybe useless
            var dropdowns = subQuestionDiv.querySelectorAll(".sub_question");

            var check_boxes = subQuestionDiv.querySelectorAll('input[type="checkbox"]');

            if(sub_questions.includes(q_id[key_i])){
                console.log("key " + q_id[key_i] + " is selected")
                subQuestionDiv.parentNode.hidden = false;
                subQuestionDiv.parentNode.classList.remove("disabled");
                /*for(let i=0;i<check_boxes.length;i++){
                    console.log("I shouldnt")
                    check_boxes[i].parentNode.hidden = false;
                }*/
                // TODO change the class as well
            }
            else{
              console.log("key " + q_id[key_i] + " is hidden")
              // hide the subquestion
                subQuestionDiv.parentNode.hidden = true;
                subQuestionDiv.parentNode.classList.add("disabled");
                // deselect the checked options of subquestions
                if(check_boxes){
                    for(let i=0;i<check_boxes.length;i++){
                        console.log(check_boxes[i].checked);
                        deselect(check_boxes[i]);
                        console.log(check_boxes[i].checked);
                    }
                }
            }
        }
    }

}
var surveyFormDOM = document.getElementById("surveyQuestions");

// this is not compatible with saved data

var subQuestions = surveyFormDOM.querySelectorAll(".subquestion");
for(i=0;i<subQuestions.length;++i) {
    if(subQuestions[i].classList.contains("disabled"))
    {
        subQuestions[i].hidden = true;
        subQuestions[i].classList.remove("disabled")
    }
    else
    {
        subQuestions[i].hidden = false;
        subQuestions[i].classList.add("disabled")

    }
};
