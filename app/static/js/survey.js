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
    console.log("selected options", stray);
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

    console.log("Relevant subquestions:" + subQuestions)
    return subQuestions;
}

function toggleVisibility(elementIdPrefix, subQuestions, subQuestionMapping) {
    for (let key in subQuestionMapping) {
        if(typeof subQuestionMapping[key] === 'string' || subQuestionMapping[key] instanceof String){
            var q_id = [subQuestionMapping[key]];
        }
        else{q_id=subQuestionMapping[key]}

        console.log("ids", q_id)

        // loop over the subquestions
        for (let key_i in q_id){
            debugger;
            var subQuestionDiv = document.getElementById(elementIdPrefix + q_id[key_i]);
            console.log("displaying subquestions for" + subQuestionDiv)
            // TODO maybe useless
            var dropdowns = subQuestionDiv.querySelectorAll(".sub_question");

            var check_boxes = subQuestionDiv.querySelectorAll('input[type="checkbox"]');

            if(subQuestions.includes(q_id[key_i])){
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
                        deselect(check_boxes[i]);
                    }
                }
            }
        }
    }
}

function triggerSubQuestion(new_value,subQuestionMapping){
    console.log("Trigger Sub Question");
    let selectedValues = getSelectedValues(new_value);
    let subQuestions = getRelevantSubQuestions(selectedValues, subQuestionMapping);
    toggleVisibility("div_id_criteria_", subQuestions, subQuestionMapping);
}

function triggerMatrixSubQuestion(new_value, subQuestionMapping) {
    console.log("Trigger Matrix SubQuestion");

    let selectedValues = getSelectedValues(new_value);
    console.log("Selected options:", selectedValues);

    let subQuestions = getRelevantSubQuestions(selectedValues, subQuestionMapping);
    console.log("Relevant SubQuestions:", subQuestions);

    // TODO this was made by chatGPT... check usefulness and if we want to take an approach like this
    // Possible approach to check for the water and assign the number of columns for the matrix...
    let waterTypeDifferentiation = document.querySelector('[name="id_criteria_2"]');
    debugger;
    let numColumns = waterTypeDifferentiation && waterTypeDifferentiation.value === "yes" ? 2 : 1;

    // ... then show the matrix rows related to the relevant questions
    toggleVisibility("matrix_row_", subQuestions, subQuestionMapping);

    // Adjust matrix column visibility
    subQuestions.forEach(q_id => {
        let matrixRow = document.getElementById("matrix_row_" + q_id);
        if (!matrixRow) return;

        let columns = matrixRow.querySelectorAll(".matrix_col");
        columns.forEach((col, idx) => {
            col.hidden = idx >= numColumns;
        });
    });
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
