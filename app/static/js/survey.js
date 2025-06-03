function deselect(elm) {
    if (elm.checked == true) {
    elm.click();
    }
}

function getSelectedValues(inputElement) {
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
    return stray
}

function getRelevantSubQuestions(selectedValues, subQuestionMapping) {
    var subQuestions = [];
    selectedValues.filter((r) => {
        // select only potential subquestions
        return r in subQuestionMapping;
    }).map((o)=>{
      // if there are more than one subquestion, expands their numbers
        if( typeof subQuestionMapping[o] != "string"){
            subQuestionMapping[o].map((e)=>{subQuestions.push(e);});
        }
        else{subQuestions.push(subQuestionMapping[o]);}
    });

    return subQuestions;
}

function toggleVisibility(elementIdPrefix, subQuestions, subQuestionMapping) {
    for (let key in subQuestionMapping) {
        if(typeof subQuestionMapping[key] === 'string' || subQuestionMapping[key] instanceof String){
            var q_id = [subQuestionMapping[key]];
        }
        else{q_id=subQuestionMapping[key]}

        // loop over the subquestions
        for (let key_i in q_id){
            var subQuestionDiv = document.getElementById(elementIdPrefix + q_id[key_i]);
            if(subQuestionDiv === null){
                subQuestionDiv = document.getElementById(elementIdPrefix + q_id[key_i]);
            }
            var dropdowns = subQuestionDiv.querySelectorAll(".sub_question");

            var check_boxes = subQuestionDiv.querySelectorAll('input[type="checkbox"]');

            if(subQuestions.includes(q_id[key_i])){
                // show the subquestion
                subQuestionDiv.parentNode.classList.remove("disabled");
            }
            else{
                // hide the subquestion
                subQuestionDiv.parentNode.classList.add("disabled");
                // deselect the checked options of subquestions
                if(check_boxes){
                    for(let i=0;i<check_boxes.length;i++){
                        deselect(check_boxes[i]);
                    }
                }
            }
        }
    }
}

function toggleMatrixVisibility(elementIdPrefix, subQuestions, subQuestionMapping) {
    let tot_selected=0;
    for (let key in subQuestionMapping) {
        if(typeof subQuestionMapping[key] === 'string' || subQuestionMapping[key] instanceof String){
            var q_id = [subQuestionMapping[key]];
        }
        else{q_id=subQuestionMapping[key]}

        let row_selected = false;
        // loop over the subquestions
        for (let key_i in q_id){

            var subQuestionDiv = document.getElementById(elementIdPrefix + q_id[key_i]);
            if(subQuestionDiv === null){
                subQuestionDiv = document.getElementById(elementIdPrefix + q_id[key_i]);
            }
            var dropdowns = subQuestionDiv.querySelectorAll(".sub_question");

            var check_boxes = subQuestionDiv.querySelectorAll('input[type="checkbox"]');

            if(subQuestions.includes(q_id[key_i])){
                // show the subquestion
                row_selected = true
                subQuestionDiv.classList.remove("disabled");
            }
            else{
                // hide the subquestion
                subQuestionDiv.classList.add("disabled");
                // deselect the checked options of subquestions
                if(check_boxes){
                    for(let i=0;i<check_boxes.length;i++){
                        deselect(check_boxes[i]);
                    }
                }
            }
        }
        if(row_selected){
        tot_selected+=1;
        }
    }

    // set parent class disabled when no one is selected
    if(tot_selected==0){
        subQuestionDiv.parentNode.hidden = true;
        subQuestionDiv.parentNode.classList.add("disabled");
    }else{
         subQuestionDiv.parentNode.hidden=false;
         subQuestionDiv.parentNode.classList.remove("disabled");
    }


}



function triggerSubQuestion(new_value,subQuestionMapping){
    console.log("Trigger Sub Question");
    let selectedValues = getSelectedValues(new_value);
    let subQuestions = getRelevantSubQuestions(selectedValues, subQuestionMapping);
    toggleVisibility("div_id_criteria_", subQuestions, subQuestionMapping);
}

function triggerMatrixSubQuestion(new_value, subQuestionMapping) {
    console.log("Trigger Matrix Sub Question");

    let selectedValues = getSelectedValues(new_value);

    let subQuestions = getRelevantSubQuestions(selectedValues, subQuestionMapping);

    // TODO this was made by chatGPT... check usefulness and if we want to take an approach like this
    // Possible approach to check for the water and assign the number of columns for the matrix...
    //let waterTypeDifferentiation = document.querySelector('[name="id_criteria_2"]');
    //debugger;
    //let numColumns = waterTypeDifferentiation && waterTypeDifferentiation.value === "yes" ? 2 : 1;
    let numColumns = 4;
    // ... then show the matrix rows related to the relevant questions
    toggleMatrixVisibility("id_criteria_", subQuestions, subQuestionMapping);
}

var surveyFormDOM = document.getElementById("surveyQuestions");

// this is not compatible with saved data

/*var subQuestions = surveyFormDOM.querySelectorAll(".subquestion");
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
};*/
